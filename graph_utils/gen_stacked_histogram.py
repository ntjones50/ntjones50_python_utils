# **************************************
# Function written by Nathan Jones
# **************************************

#------------- Imports -----------------
import pandas as pd
import plotly.graph_objects as go
from pydantic import validate_call
from typing import Optional, List, Dict
import copy
import math
import numpy as np
#------------- End Imports -------------

@validate_call(config = {'strict':True})
def gen_stacked_histogram(

    df,
    data_col: str,
    series_col: str,
    series_stacking: List[str],
    title: str,
    x_axis_label:str,
    y_axis_label:str,
    legend_label:str,
    bin_count: Optional[int] = None,
    frequency: bool = True,
    title_size: int = 30,
    x_axis_label_size: int = 25,
    y_axis_label_size: int = 25,
    legend_label_size: int = 25,
    legend_text_size: int = 18,
    x_axis_tick_label_size: int = 18,
    y_axis_tick_label_size: int = 18,
    color_dict: Optional[Dict[str,str]] = None,
    fig_width: int = 1150,
    fig_height: int = 650,
    hover_bin_decimal_places: Optional[int] = None,
    hover_val_decimal_places: Optional[int]= None,
    x_axis_tick_label_standoff: int = 15,
    y_axis_tick_label_standoff: int = 15) -> list:

    """
    The purpose of this function is to create a Plotly stacked histogram figure. The function
    takes in a Pandas DataFrame with two columns used in processing the figure. One column is of type
    float64 and holds data to be included in the histogram. The other column is of type string and 
    includes the series for each data point. Each row in the DataFrame is a single data point for
    the histogram. It is possible for all points in the DataFrame to belong to the same series,
    in which case the series column contains only a single unique string.

    Each series has the same bins. The leftmost bin starts at the overall minimum value in the data
    column (over all series). Similarly, the rightmost bin ends at the overall maximum value in the
    data column (over all series). Bins are all of equal width apart from potential floating point errors.
    The number of bins can optionally be specified by the user as an input. If unspecified, the
    number of bins is set equal to sqrt(# rows in the data column) rounded up to the nearest integer.
    This is conceptually similar to the rule of thumb presented by Jay L. Devore in the book Probability
    and Statistics For Engineering and the Sciences: Ninth Edition. For a given bin, the bars on the figure
    across series are presented as stacked.

    The y-axis on the figure is configurable using inputs and can be either frequency (i.e., number of 
    data points) or relative frequency (i.e., proportion of all data points). 

    Colors of series can optionally be specified by the user via an input dictionary.

    Inputs:

        df (pd.DataFrame) = Input Pandas DataFrame with two user-specified columns. The first, specified by
                            data_col, is of type float64 and contains data to include in the histogram. The
                            second, specified by series_col, is of type string and includes the series designator
                            for each data point. Each row in the DataFrame is a point to be included in the histogram.
                            Both the data_col and series_col columns need to be fully populated. df can have additional
                            columns, but they don't factor into the figure.

        data_col (string) = The string name of the column within df holding data.

        series_col (string) = The string name of the column within df holding series identifiers.

        series_stacking (list) = A list with a 1-to-1 match between entries and unique values in the series_col column
                                 of df. The order of a series in this list dictates where that series resides in the 
                                 stacking across bins. The first series in the list is at the bottom, the second series
                                 in the list is on top of that, etc.

        title (string) = The title for the figure to be displayed at the top center

        x_axis_label (string) = The x-axis label for the figure

        y_axis_label (string) = The y-axis label for the figure

        legend_label (string) = The legend label for the figure

        bin_count (int) = [Optional] The number of bins to include in the histogram. Defaults to None, resulting
                          in the number of bins being set to sqrt(# rows in the data_col column) rounded up to 
                          the nearest integer.

        frequency (bool) = [Optional] A boolean where True means the y-axis should be frequency and False means
                           the y-axis should be relative frequency. Defaults to True.

        title_size (int) = [Optional] The title size for the figure. Defualts to 30

        x_axis_label_size (int) = [Optional] The size of the x-axis label. Defaults to 25

        y_axis_label_size (int) = [Optional] The size of the y-axis label. Defaults to 25

        legend_label_size (int) = [Optional] The size of the legend label. Defaults to 25

        legend_text_size (int) = [Optional] The size of the legend text. Defaults to 18

        x_axis_tick_label_size (int) = [Optional] The size of x-axis tick labels. Defaults to 18

        y_axis_tick_label_size (int) = [Optional] The size of y-axis tick labels. Defaults to 18

        color_dict (dict) = [Optional] A dictionary where there is a 1-to-1 match between keys and entries in 
                            series_stacking. Each value is a string indicating the color to use for the series.
                            Defaults to None, resulting in arbitrary selection of series colors.

        fig_width (int) = [Optional] The width of the figure. Defaults to 1150

        fig_height (int) = [Optional] The height of the figure. Defaults to 650

        hover_bin_decimal_places (int) = [Optional] The number of decimal places to use for bin boundaries
                                         in the hover. Defaults to None, which mean no rounding. If set, it's
                                         recommended the user add a label to the figure indicating that bins
                                         in the hover are approximate. If set, value must be >= 1.

        hover_val_decimal_places (int) = [Optional] The number of decimal places to use for the bin relative
                                         frequencies in the hover. Can only be specified if frequency is False.
                                         Defaults to None, which means no rounding. If set, it's recommended
                                         the user add a label to the figure indicating that relative frequency
                                         values in the hover are approximate. If set, value must be >= 1.


        x_axis_tick_label_standoff (int) = [Optional] The x-axis tick label standoff. Defaults to 15.

        y_axis_tick_label_standoff (int) = [Optional] The y-axis tick label standoff. Default to 15.

    Outputs:

        This function outputs a list with two elements. The element at index 0 is the Plotly figure object.
        The element at index 1 is a list with data related to the figure. This data list has the following
        elements by index:

            [0] - (int) The number of bins used in the figure.

            [1] - (dict) A dictionary with one string key for each series name. Each value is a list containing
                  float values for bin boundaries, going from left to right (e.g., leftmost bin boundary is list
                  index 0).

            [2] - (dict) A dictionary with one string key for each series name. Each value is a list containing the
                  height value (i.e., frequency or relative frequency) for each bin from left to right (e.g.,
                  leftmost bin has index 0 in the list)
            
            [3] - (dict) A dictionary with one string key for each series name. Each value is a list containing
                  the hover text for each bin from left to right (e.g., leftmost bin has index 0 in the list)

    Testing:

        Is all the testing for this function automated with pytest (Y/N): N
        Path to automated testing file for pytest: tests/test_gen_stacked_histogram.py
        Testing description and result: On 4/26/2026, the function passed automated input check testing
                                        via pytest. Function also passed Tests 1-3 via automated pytest testing
                                        and manual inspection of the figures.

    """

    #------------------------ Input Checks -----------------------------
    # (1) df must be a Pandas DataFrame
    if not isinstance(df,pd.DataFrame):
        raise TypeError("(1) df must be a Pandas DataFrame")

    # (2) data_col needs to be a column in df
    if not data_col in list(df.columns):
        raise ValueError("(2) data_col needs to be a column in df")
    
    # (3) data_col column within df needs to be of type float64
    if not df[data_col].dtype == 'float64':
        raise TypeError("(3) data_col column within df needs to be of type float64")
    
    # (4) data_col column within df needs to be fully populated
    if not (df[data_col].count() == len(df[data_col])):
        raise ValueError("(4) data_col column within df needs to be fully populated")
    
    # (5) series_col needs to be a column in df
    if not series_col in list(df.columns):
        raise ValueError("(5) series_col needs to be a column in df")
    
    # (6) series_col column within df needs to be of type string
    if not df[series_col].dtype == 'string':
        raise TypeError("(6) series_col column within df needs to be of type string")
    
    # (7) series_col column within df needs to be fully populated
    if not (df[series_col].count() == len(df[series_col])):
        raise ValueError("(7) series_col column within df needs to be fully populated")
    
    # (8) There needs to be a 1-to-1 match between entries in series_stacking and unique values
    #     in the series_col column of df
    if not (sorted(series_stacking) == sorted(list(df[series_col].unique()))):
        raise ValueError(("(8) There needs to be a 1-to-1 match between entries in series_stacking " 
                          "and unique values in the series_col column of df"))

    # (9) If color_dict is included, there needs to be a 1-to-1 match between its keys and entries
    #     in series_stacking
    if not color_dict == None:
        if not (sorted(series_stacking) == sorted(list(color_dict.keys()))):
            raise ValueError(("(9) If color_dict is included, there needs to be a 1-to-1 match " 
                              "between its keys and entries in series_stacking"))
        
    # (10) hover_val_decimal_places can only be set if frequency = False
    if (not hover_val_decimal_places == None) and (frequency == True):
        raise ValueError("(10) hover_val_decimal_places can only be set if frequency = False")
    
    # (11) If hover_bin_decimal_places is set, value must be >= 1
    if not hover_bin_decimal_places == None:
        if not hover_bin_decimal_places >= 1:
            raise ValueError("(11) If hover_bin_decimal_places is set, value must be >= 1")
    
    # (12) If hover_val_decimal_places is set, value must be >= 1
    if not hover_val_decimal_places == None:
        if not hover_val_decimal_places >= 1:
            raise ValueError("(12) If hover_val_decimal_places is set, value must be >= 1")
    #------------------------ End Input Checks -------------------------

    # Create working copies of select inputs
    wrk_df = df.copy()
    wrk_series_stacking = copy.deepcopy(series_stacking)
    if color_dict == None:
        wrk_color_dict = None
    else:
        wrk_color_dict = copy.deepcopy(color_dict)
    
    # Determine number of bins
    if bin_count == None:
        wrk_bin_count = math.ceil(math.sqrt(float(len(wrk_df))))
    else:
        wrk_bin_count = bin_count

    # Determine min and max values in data_col column of df
    data_min = wrk_df[data_col].min()
    data_max = wrk_df[data_col].max()

    # Define list of bin boundaries going from left to right
    bin_bounds = []
    bin_width = (data_max - data_min)/float(wrk_bin_count)
    for bin_bound_ix in range(wrk_bin_count + 1):
        if not bin_bound_ix == wrk_bin_count:
            bound = data_min + float(bin_bound_ix * bin_width)
        else:
            bound = data_max
        bin_bounds.append(bound)

    # Create figure
    fig = go.Figure()

    # Create holders for out_lst items
    out_lst_bin_bounds_dict = {}
    out_lst_bin_val_dict = {}
    out_lst_hover_txt_dict = {}

    # Iterate through each series
    for cur_series in wrk_series_stacking:

        # Filter DataFrame down to just rows for the series
        filt_df = wrk_df[wrk_df[series_col] == cur_series].copy().reset_index(drop=True)

        # Compute frequency histogram data with Numpy
        np_hist, np_bin_edges = np.histogram(filt_df[data_col].to_numpy(),
                                             bins = np.array(bin_bounds),
                                             range = (data_min,data_max),
                                             density = False)
        
        # If relative frequency, calibrate np_hist
        if frequency == False:
            np_hist = np_hist / float(len(wrk_df))

        # Compute center point and width of each numpy bin
        np_bin_centers = []
        np_bin_widths = []
        for bin_ix in range(wrk_bin_count):
            np_bin_center = np_bin_edges[bin_ix] + ((np_bin_edges[bin_ix + 1] - np_bin_edges[bin_ix])/2.0)
            np_bin_width = (np_bin_edges[bin_ix + 1] - np_bin_edges[bin_ix])
            np_bin_centers.append(np_bin_center)
            np_bin_widths.append(np_bin_width)

        #----------------------------------
        # Compute bin hovers
        bin_hovers = []
        y_term = 'Freq.' if frequency == True else 'Relative Freq.'
     
        for bin_ix in range(wrk_bin_count):

            bin_close = "]" if bin_ix == (wrk_bin_count - 1) else ")"

            bin_start = (np_bin_edges[bin_ix] if hover_bin_decimal_places == None else 
                        round(np_bin_edges[bin_ix], hover_bin_decimal_places))
            
            bin_stop = (np_bin_edges[bin_ix + 1] if hover_bin_decimal_places == None else 
                        round(np_bin_edges[bin_ix + 1], hover_bin_decimal_places))
            
            bin_val = (np_hist[bin_ix] if hover_val_decimal_places == None else
                       round(np_hist[bin_ix], hover_val_decimal_places))
            
            hover_text = "{}: bin [{},{}{} -> {} = {}".format(cur_series,
                                                              bin_start,
                                                              bin_stop,
                                                              bin_close,
                                                              y_term,
                                                              bin_val)

            bin_hovers.append(hover_text)
        #----------------------------------

        #----------------------------------
        # Add series to figure

        if color_dict == None:

            fig.add_trace(go.Bar(
                x = np_bin_centers,
                y = np_hist,
                name = cur_series,
                width = np_bin_widths,
                hovertext = bin_hovers))

        else:

            fig.add_trace(go.Bar(
                x = np_bin_centers,
                y = np_hist,
                name = cur_series,
                width = np_bin_widths,
                marker_color = color_dict[cur_series],
                hovertext = bin_hovers))
        #----------------------------------

        # Save values for output list
        out_lst_bin_bounds_dict[cur_series] = copy.deepcopy(np_bin_edges.tolist())
        out_lst_bin_val_dict[cur_series] = copy.deepcopy(np_hist.tolist())
        out_lst_hover_txt_dict[cur_series] = copy.deepcopy(bin_hovers)

    # Set bins to be stacked
    fig.update_layout(barmode = 'stack')

    # Set title
    fig.update_layout(title = {'text': title, 'font': {'size': title_size}, 'x': 0.5})

    # Add X-Axis Label
    fig.update_layout(xaxis_title = x_axis_label, xaxis_title_font = dict(size = x_axis_label_size))

    # Add Y-Axis Label
    fig.update_layout(yaxis_title = y_axis_label, yaxis_title_font = dict(size = y_axis_label_size))

    # Set x-axis tick label size and standoff
    fig.update_layout(xaxis = dict(tickfont = dict(size = x_axis_tick_label_size),
                                   ticklabelstandoff = x_axis_tick_label_standoff))
   
    # Set y-axis tick label size and standoff. If frequency, have y-axis ticks only be integers
    if frequency == False:
        fig.update_layout(yaxis = dict(tickfont = dict(size = y_axis_tick_label_size),
                                       ticklabelstandoff = y_axis_tick_label_standoff))
    else:
        fig.update_layout(yaxis = dict(tickfont = dict(size = y_axis_tick_label_size),
                                       ticklabelstandoff = y_axis_tick_label_standoff,
                                       tickformat="d", dtick = 1))

    # Set Legend
    fig.update_layout(legend = dict(title = legend_label, title_font = dict (size = legend_label_size), 
                                    font = dict(size = legend_text_size)))

    # Set figure size
    fig.update_layout(width = fig_width, height = fig_height)

    # return statement
    out_lst = [wrk_bin_count, out_lst_bin_bounds_dict, out_lst_bin_val_dict, out_lst_hover_txt_dict]
    return [fig, out_lst]
    