# **************************************
# Function written by Nathan Jones
# **************************************

#------------ Define Imports -----------
import pandas as pd
from pandas import DataFrame as df
import plotly.graph_objects as go
import copy
#---------------------------------------

def gen_multi_series_scatter_plot(in_df: df, series_col: str, x_data_col: str, y_data_col: str,
                                  title: str, x_axis_label: str, y_axis_label: str, legend_label: str, 
                                  x_axis_range: list = [], y_axis_range: list = [],  color_dict: dict = {}, 
                                  pt_size: int = 15) -> go.Figure:

    '''
    Description:

    The purpose of this function is to generate a Plotly scatter plot displaying one or more series of data 
    where each displayed point has an x and y coordinate. Point colors denote the series they belong to on
    the plot. The function takes as input a Pandas dataframe with 3 or more columns. The x_data_col and 
    y_data_col columns hold the x and y coordinates of points to plot, respectively. These columns must be 
    either int64 or float64. The series_col must be of type string and provides the series for each point.
    A single series can be plotted by including a constant value in series_col. Across the 3 columns, a single 
    row in the input DataFrame holds information for a single point to be plotted. Additional inputs 
    are available for a user to tailor the plot.
    
    Inputs:

        in_df (Pandas DataFrame) =  The source Pandas DataFrame for the plot. The DataFrame must have at least 
                                    3 columns. Each row in the DataFrame is a point to be plotted. One column, 
                                    specified in series_col, is of type string and holds the series for each 
                                    point. Columns specified by x_data_col and y_data_col hold x and y coordinates
                                    for the points, respectively. These column must be either int64 or float64.
                                    All 3 user specified columns must be fully populated. The DataFrame can 
                                    have more than 3 columns, but columns beyond the 3 specified don't factor 
                                    into the plotting. All column names must be of string form.

        series_col (string) = A string holding the name of the column within in_df that holds series identifiers
                              for each row.

        x_data_col (string) = A string holding the name of the column within in_df that holds x-coordinates for 
                              points to plot.

        y_data_col (string) = A string holding the name of the column within in_df that holds y-coordinates for 
                              points to plot

        title (string) = A string holding the title to be displayed on the plot

        x_axis_label (string) = A string holding the x-axis label to be displayed for the plot

        y_axis_label (string) = A string holding the y-axis label to be displayed for the plot

        legend_label (string) = A string holding the legend label to be displayed for the plot

        x_axis_range (list) = [Optional] A list specifying the [minimum, maximum] for the x-axis on the plot.
                              If included, the minimum and maximin must be int if x_data_col is int64 or float
                              if x_data_col is float64. Further, all x-coordinates must be between the minimum 
                              and maximum, and cannot be equal to either bound. If not included, Plotly chooses 
                              the axis bounds.

        y_axis_range (list) = [Optional] A list specifying the [minimum, maximum] for the y-axis on the plot.
                              If included, the minimum and maximin must be int if y_data_col is int64 or float
                              if y_data_col is float64. Further, all y-coordinates must be between the minimum 
                              and maximum, and cannot be equal to either bound. If not included, Plotly chooses 
                              the axis bounds.

        color_dict (dict) = [Optional] A dictionary where each key is a string representing a series within 
                            series_col and each value is a string representing a color. If the dictionary is
                            included, all series within series_col need to be present. If not included, Plotly
                            chooses the colors.
        
        pt_size (int) = [Optional] The size of points to plot. If not included, defaults to 15.
                                    
        
    Outputs:

        fig (go.Figure)  =   The generated figure

    Testing:

        Is all the testing for this function automated with pytest (Y/N): N
        Path to automated testing file for pytest: tests/test_gen_multi_series_scatter_plot.py
        Non-pytest testing description and result: Charts were generated for each of 9 test cases 
                                                   in the pytest testing file. All charts were 
                                                   manually reviewed and confirmed to be correct.

    '''

    #---------------------------------- CONFIRM USER INPUTS -------------------------------------
    
    # Ensure in_df is a DataFrame
    if not isinstance(in_df, df):
        raise Exception("in_df needs to be a Pandas DataFrame")
    
    # Ensure series_col is a string
    if not isinstance(series_col, str):
        raise Exception("series_col needs to be a string")
    
    # Ensure series_col is a series in in_df
    if not series_col in in_df.columns:
        raise Exception("series_col needs to be a column in in_df")
    
    # Ensure series_col in in_df is of type string
    if not in_df[series_col].dtype == 'string':
        raise Exception('series_col in in_df needs to be of type string')

    # Ensure series_col is fully populate in in_df
    if not len(in_df[series_col]) == in_df[series_col].count():
        raise Exception("series_col within in_df needs to be fully populated")
    
    # Ensure x_data_col is a string
    if not isinstance(x_data_col,str):
        raise Exception("x_data_col needs to be a string")
    
    # Ensure x_data_col is a column in in_df
    if not x_data_col in in_df.columns:
        raise Exception("x_data_col needs to be a column in in_df")
    
    # Ensure x_data_col in in_df is of type int64 or float64
    if not (in_df[x_data_col].dtype == 'int64' or in_df[x_data_col].dtype == 'float64'):
        raise Exception('x_data_col in in_df needs to be of type int64 or float64')

    # Ensure x_data_col is fully populate in in_df
    if not len(in_df[x_data_col]) == in_df[x_data_col].count():
        raise Exception("x_data_col within in_df needs to be fully populated")

    # Ensure y_data_col is a string
    if not isinstance(y_data_col, str):
        raise Exception("y_data_col needs to be a string")
    
    # Ensure y_data_col is a column in in_df
    if not y_data_col in in_df.columns:
        raise Exception("y_data_col needs to be a column in in_df")
    
    # Ensure y_data_col in in_df is of type int64 or float64
    if not (in_df[y_data_col].dtype == 'int64' or in_df[y_data_col].dtype == 'float64'):
        raise Exception('y_data_col in in_df needs to be of type int64 or float64')

    # Ensure y_data_col is fully populate in in_df
    if not len(in_df[y_data_col]) == in_df[y_data_col].count():
        raise Exception("y_data_col within in_df needs to be fully populated")
    
    # Ensure title is a string
    if not isinstance(title, str):
        raise Exception("Title needs to be a string")
    
    # Ensure x_axis_label is a string
    if not isinstance(x_axis_label, str):
        raise Exception("x_axis_label needs to be a string")
    
    # Ensure y_axis_label is a string
    if not isinstance(y_axis_label, str):
        raise Exception("y_axis_label needs to be a string")
    
    # Ensure legend_label is a string
    if not isinstance(legend_label, str):
        raise Exception("legend_label needs to be a string")
    
    # If provided, ensure x_axis_range is a list
    if not x_axis_range == []:
        if not isinstance(x_axis_range, list):
            raise Exception("x_axis_range needs to be a list")
    
    # If provided, ensure y_axis_range is a list
    if not y_axis_range == []:
        if not isinstance(y_axis_range, list):
            raise Exception("y_axis_range needs to be a list")
        
    # If provided, ensure, x_axis range has two entries 
    if not x_axis_range == []:
        if not len(x_axis_range) == 2:
            raise Exception ("x_axis_range must have 2 entries")
    
    # If provided, ensure, y_axis range has two entries 
    if not y_axis_range == []:
        if not len(y_axis_range) == 2:
            raise Exception ("y_axis_range must have 2 entries")
        
    # If provided, ensure, x_axis range entry types match x_data_col
    if not x_axis_range == []:
        if not ((isinstance(x_axis_range[0], float) and isinstance(x_axis_range[1], float) and 
                 in_df[x_data_col].dtype == 'float64') or ((isinstance(x_axis_range[0], int) and 
                 isinstance(x_axis_range[1], int) and in_df[x_data_col].dtype == 'int64'))):
            raise Exception ("x_axis_range values must be of comparable type to the in_df x_data_col")
    
    # If provided, ensure, y_axis range entry types match y_data_col
    if not y_axis_range == []:
        if not ((isinstance(y_axis_range[0], float) and isinstance(y_axis_range[1], float) and 
                 in_df[y_data_col].dtype == 'float64') or ((isinstance(y_axis_range[0], int) and 
                 isinstance(y_axis_range[1], int) and in_df[y_data_col].dtype == 'int64'))):
            raise Exception ("y_axis_range values must be of comparable type to the in_df y_data_col")
        
    # If provided, ensure all x_data_col values are within the range of x_axis_range exclusive of bounds
    if not x_axis_range == []:
        if not (in_df[x_data_col].min() > x_axis_range[0] and in_df[x_data_col].max() < x_axis_range[1]):
            raise Exception('All values in the x_data_col of in_df must be within the bounds of x_axis_range exclusive of the bounds')

    # If provided, ensure all y_data_col values are within the range of y_axis_range exclusive of bounds
    if not y_axis_range == []:
        if not (in_df[y_data_col].min() > y_axis_range[0] and in_df[y_data_col].max() < y_axis_range[1]):
            raise Exception('All values in the y_data_col of in_df must be within the bounds of y_axis_range exclusive of the bounds')

    # If provided, ensure color_dict is a dictionary
    if not color_dict == {}:
        if not isinstance(color_dict, dict):
            raise Exception('color_dict must be a dictionary')
    
    # If provided, ensure each key in color_dict is a string
    if not color_dict == {}:
        for i in color_dict.keys():
            if not isinstance(i, str):
                raise Exception('All keys in color_dict must be strings')
    
    # If provided, ensure each value in color_dict is a string
    if not color_dict == {}:
        for i in color_dict.keys():
            if not isinstance(color_dict[i], str):
                raise Exception('All values in color_dict must be strings')
    
    # If provided, make sure each key in color_dict is a series in series_col and all series in 
    # series_col are accounted for
    if not color_dict == {}:
        if not len(color_dict) == len(in_df[series_col].unique()):
            raise Exception('All series need to be accounted for in color_dict')
        for i in color_dict.keys():
            if not i in in_df[series_col].unique():
                raise Exception('All keys in color_dict need to be series in the series_col column')        

    # Ensure pt_size is an int if provided
    if not pt_size == 15:
        if not isinstance(pt_size, int):
            raise Exception("pt_size needs to be an int")
    #---------------------------------- END CONFIRM USER INPUTS ---------------------------------

    # Create working version of key inputs
    wrk_df = in_df.copy()
    wrk_x_axis_range = copy.deepcopy(x_axis_range)
    wrk_y_axis_range = copy.deepcopy(y_axis_range)
    wrk_color_dict = copy.deepcopy(color_dict)
    wrk_title = title

    # Create Figure
    fig = go.Figure()

    # Extract series
    series = wrk_df[series_col].unique()

    # Iterate through each series
    for s in series:

        # Filter wrk_df to just rows for the series
        filter_df = wrk_df[wrk_df[series_col] == s].copy()

        # Add data to figure
        if not wrk_color_dict == {}:
            fig.add_trace(go.Scatter(x = filter_df[x_data_col], y = filter_df[y_data_col], mode = 'markers',
                                    name = s, marker = dict(size = pt_size, color = wrk_color_dict[s])))
        else:
            fig.add_trace(go.Scatter(x = filter_df[x_data_col], y = filter_df[y_data_col], mode = 'markers',
                                    name = s, marker = dict(size = pt_size)))
        
    # Add Title
    fig.update_layout(title = {'text': wrk_title, 'font': {'size': 30}, 'x': 0.5})

    # Add X-Axis Label
    fig.update_layout(xaxis_title = x_axis_label, xaxis_title_font = dict(size = 25))

    # Add Y-Axis Label
    fig.update_layout(yaxis_title = y_axis_label, yaxis_title_font = dict(size = 25))

    # If provided, set x-axis range
    if not x_axis_range == []:
        fig.update_layout(xaxis = dict(range = x_axis_range))

    # If provided, set y-axis range
    if not y_axis_range == []:
        fig.update_layout(yaxis = dict(range = y_axis_range))

    # Set x-axis tick size and tick standoff
    fig.update_layout(xaxis = dict(tickfont = dict(size = 20)))
    fig.update_xaxes(ticklabelstandoff = 10)

    # Set y-axis tick size and tick standoff
    fig.update_layout(yaxis = dict(tickfont = dict(size = 20)))
    fig.update_yaxes(ticklabelstandoff = 10)

    # Lock Axes
    fig.update_xaxes(fixedrange = True)
    fig.update_yaxes(fixedrange = True)

    # Set figure size
    fig.update_layout(width = 900, height = 600)

    # Set Legend
    fig.update_layout(legend = dict(title = legend_label, title_font = dict (size = 22), 
                                    font = dict(size = 20)))

    # Return figure
    return fig