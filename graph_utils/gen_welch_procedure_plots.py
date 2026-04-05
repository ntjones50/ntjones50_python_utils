# **************************************
# Function written by Nathan Jones
# **************************************

#------------ Define Imports -----------
import pandas as pd
from pandas import DataFrame as df
import plotly.graph_objects as go
import copy
import math
#---------------------------------------

def gen_welch_procedure_plots(in_df: df, rep_col: str, time_step_col: str, metric_col: str,
                              n: int, m: int, time_step_units: str, units_per_timestep: float, 
                              first_timestep_units: float, metric_name: str = None,
                              w: int = None, x_axis_units = True) -> list:
    
    """
    Description:

    The purpose of this function is to aid in identifying the length of a warmup period (l) for use
    in conducting steady-state analysis with simulation output data. This is accomplished via 
    implementing Welch's procedure as presenting in the book "Simulation Modeling and Analysis: 
    6th Edition" by Averill M. Law p.407-409. 

    This function assumes n simulation replications (recommended >= 5) have been conducted where
    each replication is run for m timesteps (m is large). It is assumed that a metric of interest 
    has been recorded for each combination of replication and timestep. 

    The function takes in a Pandas Dataframe where each row corresponds to a combination of replication
    and timestep. The DataFrame has at least 3 column. 3 of the columns are user specified and 
    correspond to the replication number, timestep number, and metric value respectively. Replications
    are numbered 1, 2, ..., n, and the associated column must be int64 and fully populated. The timestep 
    column must be int64 and timesteps take on values 1, 2, ..., m. The metric column must be int64 or 
    float64 and fully populated.

    The function retuns a list with 2 plots. The index 0 plot gives the average metric value over all
    replications (y-axis) over timesteps (x-axis). This index 0 plot is not a moving average. The 
    index 1 plot gives a moving average of the timestep average metric values (y-axis) over timesteps
    (x-axis). A user can use the index 1 plot to identify the warmup period l, such that l is the 
    timestep value beyond which the moving averages converge (See Law p.408).
    
    Inputs:
            in_df (Pandas DataFrame): The source Pandas DataFrame holding simulation output. Each row 
                                      in the DataFrame corresponds to a combination of simulation 
                                      replication and timestep. The DataFrame has a minimum of 3 
                                      columns. The first user specified column, noted in rep_col, gives
                                      the replication. This column is fully populated and takes values,
                                      1, 2, ... n. The second user specified column, noted in 
                                      time_step_col must be of form int64 and fully populated. 
                                      The third user specified column, noted in metric_col, holds 
                                      simulation output metrics, must be fully populated, and needs to 
                                      be int64 or float64. The DataFrame can have more than 3 columns, 
                                      but those beyond the user specified columns will be ignored by the 
                                      function. Column names must be string form.
            
            rep_col (string): Name of the column within in_df holding replication data.

            time_step_col (string): Name of the column within in_df holding timesteps.

            metric_col (string): Name of the column within in_df holding metric values.

            n (int): The number of simulation replications included in in_df.

            m (int): The maximum timestep in the simulation replications.

            time_step_units (string): The units associated with timesteps (e.g., if each timestep is 
                                      2.5 hours, this would be 'Hours')
            
            units_per_timestep (float): The number of units per timestep (e.g., if each timestep is 
                                        2.5 hours, this would be 2.5)

            first_timestep_units (float): The number of units associated with timestep 1. (e.g., if each 
                                          timestep is 2.5 hours you may want timestep 1 to be 0.0 
                                          units or 2.5 units)
        
            metric_name (string): (Optional) A name for the metric to use in the plots

            w (int): (Optional) The number of timesteps for the moving-average window for
                                the index 1 plot. If not provided, value defaults to the floor(# of 
                                timesteps in replication / 4)
            
            x_axis_units (bool): (Optional) True means you want the plot x-axis values in units. False 
                                            means you want the values in timesteps. Defaults to True
    
    Outputs:

            out_lst (List): A list containing 2 Plotly figures as outlined in the description
                            above at indices 0 and 1. At index 2, the list holds a list with data for
                            testing. Values within this index 2 list are:

                                [0] - list of replications
                                [1] - list of timesteps
                                [2] - list to hold metric mean over replications by timestep
                                [3] - w
                                [4] - list containing moving average values for the first timestep 
                                      to the m-w timestep
                                [5] - x coordinates for figure at index 0
                                [6] - x coordinates for figure at index 1

    Testing:

        Is all the testing for this function automated with pytest (Y/N):  N
        Path to automated testing file for pytest: /tests/test_gen_welch_procedure_plots.py
        Non-pytest testing description and result: Plots produced by tests were visually
                                                   inspected and confirmed to be correct
    """

    #------------------ Confirm User Inputs -----------------------
    # in_df needs to be a DataFrame
    if not isinstance(in_df, df):
        raise Exception("in_df needs to be a Pandas DataFrame")
    
    # rep_col needs to be a string
    if not isinstance(rep_col,str):
        raise Exception("rep_col needs to be a string")
    
    # rep_col needs to be a column within in_df
    if not rep_col in in_df.columns:
        raise Exception("rep_col needs to be the name of a column within in_df")
    
    # The rep_col column within in_df needs to be int64
    if not in_df[rep_col].dtype == 'int64':
        raise Exception('rep_col within in_df needs to be int64')
    
    # time_step_col needs to be a string
    if not isinstance(time_step_col,str):
        raise Exception('time_step_col needs to be a string')
    
    # time_step_col needs to be a column in in_df
    if not time_step_col in in_df.columns:
        raise Exception('time_step_col needs to be a column within in_df')
    
    # The time_step_col in in_df needs to be int64
    if not in_df[time_step_col].dtype == 'int64':
        raise Exception('The time_step_col column in in_df needs to be of type int64')
    
    # metric_col needs to be a string
    if not isinstance(metric_col,str):
        raise Exception('metric_col needs to be a string')
    
    # metric_col needs to be a column within in_df
    if not metric_col in in_df.columns:
        raise Exception('metric_col needs to be a column within in_df')
    
    # metric_col column in in_df needs to be int64 or float64
    if not (in_df[metric_col].dtype == 'int64' or in_df[metric_col].dtype == 'float64'):
        raise Exception('The metric_col column within in_df needs to be int64 or float64')

    # if metric_col column in in_df is float64 it needs to be fully populated
    if not len(in_df[metric_col]) == in_df[metric_col].count():
        raise Exception('The metric col column within in_df needs to be fully populated')
    
    # n needs to be an int
    if not isinstance(n,int):
        raise Exception('n needs to be of type int')
    
    # n needs to be the maximum replication
    if not int(n) == int(in_df[rep_col].max()):
        raise Exception('n needs to be the maximum replication number in in_df') 
    
    # m needs to be an int
    if not isinstance(m,int):
        raise Exception('m needs to be of type int')
    
    # m needs to be the maximum timestep
    if not int(m) == int(in_df[time_step_col].max()):
        raise Exception('m needs to be the maximum timestep within in_df')
    
    # time_step_units needs to be a string
    if not isinstance(time_step_units,str):
        raise Exception('time_step_units needs to be of type str')
    
    # units_per_timestep needs to be a float
    if not isinstance(units_per_timestep,float):
        raise Exception('units_per_timestep needs to be a float')
    
    # first_timestep_units needs to be a float
    if not isinstance(first_timestep_units,float):
        raise Exception('first_timestep_units needs to be a float')
    
    # If provided, metric_name needs to be a string
    if not metric_name == None:
        if not isinstance(metric_name,str):
            raise Exception('metric_name needs to be a string if provided')
    
    # if w is provided it needs to be an int
    if not w == None:
        if not isinstance(w,int):
            raise Exception('w needs to be an int if provided')
    
    # x_axis_units needs to be a boolean
    if not isinstance(x_axis_units,bool):
        raise Exception('x_axis_units needs to be a bool')
    
    # make sure in_df has the correct number of rows
    if not len(in_df) == n*m:
        raise Exception("m and n don't match with the number of rows in in_df")
    
    # Create working dataframe
    wrk_df = in_df.copy()

    # make sure the replication numbers are correct within in_df
    for i in wrk_df[rep_col].unique().tolist():
        if not len(wrk_df[wrk_df[rep_col] == i]) == m:
            raise Exception("in_df has the wrong number of rows for replication {}".format(i))
        
    # make sure the timesteps are correct within in_df
    for i in wrk_df[rep_col].unique().tolist():
        temp_filter = wrk_df[wrk_df[rep_col]==i].copy().reset_index(drop=True)
        if not sorted(temp_filter[time_step_col].tolist()) == sorted(range(1,m+1,1)):
            raise Exception("in_df has incorrect timesteps for replication {}".format(i))
    #------------------ End Confirm User Inputs -------------------

    # Convert metric column to float
    wrk_df[metric_col] = wrk_df[metric_col].astype('float64')

    # Define list to return
    return_lst = []

    # Define output list
    out_lst = []

    # Get list of replications
    reps = sorted(wrk_df[rep_col].unique().tolist())
    out_lst.append(copy.deepcopy(reps))
    
    # Get list of timesteps
    timesteps = sorted(wrk_df[time_step_col].unique().tolist())
    out_lst.append(copy.deepcopy(timesteps))

    # Create list to hold metric mean over replications by timestep
    timestep_means = []

    # Iterate through timesteps
    for t in timesteps:

        # Filter DataFrame down to just rows for the timestep
        ts_filter_df = wrk_df[wrk_df[time_step_col] == t].copy().reset_index(drop=True)

        # Add the mean value to the list
        timestep_means.append(float(ts_filter_df[metric_col].mean()))

    # Store timestep_means for output
    out_lst.append(copy.deepcopy(timestep_means))

    # If needed, compute w
    if w == None:
        w = math.floor(m/4)
    
    # Save w
    out_lst.append(w)
    
    # Compute list containing moving average values for the first timestep to the m-w timestep
    moving_avgs = []
    for t in timesteps:

        # Only compute if t <= m-w
        if t <= (m - w):

            if t <= w:
                cur_mvg_avg = float(sum(timestep_means[0:((2*t)-1)]))/float((2*t-1))
            else:
                cur_mvg_avg = float(sum(timestep_means[(t-w-1):(t+w)]))/float((2*w)+1.0)
            
            moving_avgs.append(float(cur_mvg_avg))
    
    # Store moving_avgs
    out_lst.append(copy.deepcopy(moving_avgs))

    #----------------------- Build index 0 chart -----------------------------
    # Create figure
    fig_0 = go.Figure()

    # Compute plot x values
    plot_x = []
    if x_axis_units:
        first_t = True
        for t in timesteps:
            if first_t:
                plot_x.append(float(first_timestep_units))
                first_t = False
            else:
                plot_x.append(float(plot_x[len(plot_x)-1]) + float(units_per_timestep))
    else:
       for t in timesteps:
           plot_x.append(float(t))
    
    # Store plot x values
    out_lst.append(copy.deepcopy(plot_x))

    # Add data to plot
    fig_0.add_trace(go.Scatter(x = copy.deepcopy(plot_x), y = copy.deepcopy(timestep_means), mode = 'lines+markers'))

    # Get name for metric 
    if not metric_name == None:
        metric_n = metric_name
    else:
        metric_n = "Metric"

    # Add Title
    fig_0.update_layout(title = {'text': '{} Mean over Replications by Timestep'.format(metric_n),
                                 'font': {'size': 30}, 'x': 0.5})

    # Add X-Axis Label
    if x_axis_units:
        fig_0.update_layout(xaxis_title = time_step_units, 
                          xaxis_title_font = dict(size = 25))
    else:
        fig_0.update_layout(xaxis_title = "Timestep", 
                          xaxis_title_font = dict(size = 25))

    # Add Y-Axis Label
    fig_0.update_layout(yaxis_title = "{} Mean over {} Replications".format(metric_n,n), 
                        yaxis_title_font = dict(size = 25))
    
    # Set x-axis tick size and tick standoff
    fig_0.update_layout(xaxis = dict(tickfont = dict(size = 20)))
    fig_0.update_xaxes(ticklabelstandoff = 10)

    # Set y-axis tick size and tick standoff
    fig_0.update_layout(yaxis = dict(tickfont = dict(size = 20)))
    fig_0.update_yaxes(ticklabelstandoff = 10)

    # Lock Axes
    fig_0.update_xaxes(fixedrange = True)
    fig_0.update_yaxes(fixedrange = True)

    # Set figure size
    fig_0.update_layout(width = 900, height = 600)
    #----------------------- End build index 0 chart ------------------------

    #----------------------- Build index 1 chart -----------------------------
    # Create figure
    fig_1 = go.Figure()

    # Compute plot x values
    plot_x_2 = plot_x[:m - w]
    out_lst.append(copy.deepcopy(plot_x_2))

    # Add data to plot
    fig_1.add_trace(go.Scatter(x = copy.deepcopy(plot_x_2), y = copy.deepcopy(moving_avgs), mode = 'lines+markers'))

    # Add Title
    fig_1.update_layout(title = {'text': 'Moving Average of Timestep Mean {} by Timestep'.format(metric_n),
                                 'font': {'size': 30}, 'x': 0.5})
    
    # Add X-Axis Label
    if x_axis_units:
        fig_1.update_layout(xaxis_title = time_step_units, 
                          xaxis_title_font = dict(size = 25))
    else:
        fig_1.update_layout(xaxis_title = "Timestep", 
                          xaxis_title_font = dict(size = 25))

    # Add Y-Axis Label
    fig_1.update_layout(yaxis_title = "Moving Average", 
                        yaxis_title_font = dict(size = 25))
    
    # Set x-axis tick size and tick standoff
    fig_1.update_layout(xaxis = dict(tickfont = dict(size = 20)))
    fig_1.update_xaxes(ticklabelstandoff = 10)

    # Set y-axis tick size and tick standoff
    fig_1.update_layout(yaxis = dict(tickfont = dict(size = 20)))
    fig_1.update_yaxes(ticklabelstandoff = 10)

    # Lock Axes
    fig_1.update_xaxes(fixedrange = True)
    fig_1.update_yaxes(fixedrange = True)

    # Set figure size
    fig_1.update_layout(width = 900, height = 600)
    #----------------------- End build index 1 chart -----------------------------

    # Return values
    return [fig_0,fig_1,out_lst]