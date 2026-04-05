# **************************************
# Function written by Nathan Jones
# **************************************

#------------ Define Imports -----------
import pandas as pd
from pandas import DataFrame as df
import plotly.graph_objects as go
import copy
#------------ End Define Imports -------

def gen_parallel_coords_fig(
        in_df: pd.DataFrame,
        in_var_cols: list,
        in_color_col: str,
        in_fig_title: str,
        in_legend_title: str,
        in_colors: dict = None,
        in_colorscale: str = None,
        in_fig_title_size: int = 30,
        in_variable_rename: dict = None,
        in_variable_name_size: int = 20,
        in_tick_label_size: int = 15,
        in_legend_size: int = 20,
        in_str_var_orders: dict = None,
        in_fig_width: int = 1150,
        in_fig_height: int = 690) -> go.Figure:

    """
    Description:

    The purpose of this function is to generate a Plotly parallel coordinates figure, which is useful in 
    determining patterns in the values over a set of variables. One specific use case would be, in a design 
    of experiment, visualizing how the interaction of multiple factors impacts an outcome variable. 

    This function takes in a Pandas Dataframe where each row is a line to include in the parallel coordinate figure.
    The function also takes in a list containing an ordered set of column names from the DataFrame. These columns 
    contain the variable values that will be plotted on the figure for each row. The order of column names in the
    list determine order of display on the chart, both from left to right (e.g., the first column name in the list is the 
    left most column displayed in the figure). Column types can be string, int64, or float64. Thus, variables can be 
    either numeric or categorical.

    Lines are colored according to one of the variable columns or a non-variable column from the input
    DataFrame. The color column must be of type int64, float64, or string. If the color column is of type string, the
    user must feed in a dictionary specifying the color for each unique value. If the column is of type int64 or float64, 
    the user can feed in a color scale name.

    Other formatting options are present as inputs to the function.
    
    Inputs:

        in_df (Pandas DataFrame) =  The source Pandas DataFrame for the figure. Each row in the DataFrame is a line 
                                    to be plotted. The in_var_cols list contains the names of columns within in_df 
                                    that hold variable values to plot for lines. Each of these column within in_df 
                                    must be fully populated and of type int64, float64, or string. The user also specifies
                                    the name of a column to dictate line coloring via the input in_color_col. This column
                                    must also be fully populated and of type int64, float64, or string. The names of all 
                                    user specified columns must be string representations. Columns beyond those specified 
                                    by the user can be present within in_df, but they don't factor into the figure. 
                                    
         in_var_cols (list) = List of strings where each entry is the name of a column within in_df holding the values of 
                              a variable for each plotted line. The order of a column within this list determines the order
                              of plotting for the respective variable (i.e., the first column in the list is the leftmost
                              variable to be plotted).

        in_color_col (string) = The name of the column within in_df whose values should use used for coloring lines. 
                                This column can be within in_var_cols or can be a separate column.

        in_fig_title (string) = The title for the figure displayed at the top center. 

        in_legend_title (string) = Title for the legend.

        in_colors (dict) = [Optional] If the column specified within in_color_col is of type string, a user must 
                           provide this dictionary to define colors for values within the column. Each key must 
                           be a string and a unique value within the in_col_color column. All unique values
                           in the column must have one key. Values are strings defining the color for the key. 
                           The dictionary can only be provided if the in_color_col column is of type string. 
                           Default = None.

        in_colorscale (string) = [Optional] If the column specified within in_color_col is of type int64 or float64, 
                                 the user may provide a string defining the colorscale. A colorscale cannot be provided if
                                 the column specified within in_color_col is a string. If the column specified within 
                                 in_color_col is of type int64 or float64 and in_colorscale is not provided, the value
                                 defaults to Viridis.

        in_fig_title_size (int) = [Optional] The size of the figure title. Default = 30

        in_variable_rename (dict) = [Optional] A dictionary used for renaming the variables within in_var_cols for
                                    the display. If provided, each key is a string entry in in_var_cols and each value 
                                    is the string display name.

        in_variable_name_size (int) = [Optional] The size of the variable names to be displaying the in the figure.
                                      Default = 20.
        
        in_tick_label_size (int) = [Optional] The size of the tick labels in the figure. Default = 15.

        in_legend_size (int) = [Optional] The size of the legend. Default = 20

        in_str_var_orders (dict) = [Optional] If one of the columns specified in in_var_cols is of type string, the user
                                   can provide this input. Each key is the name of a column within in_var_cols of type string.
                                   Each value is a list for the corresponding key that holds all unique entries within the 
                                   associated column. The position in the list corresponds to the position of the unique entry 
                                   on the plot such that the first list entry will be at the top, the second is the first 
                                   down from the top, etc. Entries within in_var_cols corresponding to string columns can
                                   be omitted from keys and the dictionary can always be omitted. Entries within in_var_cols
                                   corresponding to string columns where there is no dictionary and key will have their 
                                   unique value positions on the plot chosen arbitrarily.

        in_fig_width (int) = [Optional] The width of the figure. Defaults to 1150

        in_fig_height (int) = [Optional] The height of the figure. Defaults to 690

    Outputs:

        fig (go.Figure)  =   The generated figure

    Testing:

        Is all the testing for this function automated with pytest (Y/N): N
        Path to automated testing file for pytest: tests/test_gen_parallel_coords_fig.py
        Date function initially passed pytest testing: 3/27/2026
        Date non-pytest testing initially passed: 3/27/2026
        Non-pytest testing description and result: Charts generated by 4 tests all passed manual
                                                   review initially on 3/27/2026
    """
    #----------------- Confirm Input Variables ------------------

    # (1) in_df must be a Pandas Dataframe
    if not isinstance(in_df, pd.DataFrame):
        raise Exception("in_df must be a Pandas Dataframe")

    # (2) in_var_cols must be a list
    if not isinstance(in_var_cols, list):
        raise Exception("in_var_cols must be a list")

    # (3) Each entry in in_var_cols needs to be a string
    for i in in_var_cols:
        if not isinstance(i,str):
            raise Exception("Each entry in in_var_cols needs to be a string")

    # (4) Each entry in in_var_cols needs to be a column within in_df
    for i in in_var_cols:
        if not i in in_df.columns:
            raise Exception("Each entry in in_var_cols needs to be a column within in_df")

    # (5) Each entry in in_var_cols needs to correspond to a column within in_df that is of type 
    #     string, int64, or float64
    for i in in_var_cols:
        if not (in_df[i].dtype == 'string[python]' or in_df[i].dtype == 'int64' or  in_df[i].dtype == 'float64'):
            raise Exception("Each entry in in_var_cols needs to correspond to a column within in_df that is of type string, int64, or float64") 

    # (6) Each entry in in_var_cols needs to correspond to a column within in_df that is fully populated
    for i in in_var_cols:
        if not in_df[i].count() == len(in_df[i]):
            raise Exception("Each entry in in_var_cols needs to correspond to a column within in_df that is fully populated")

    # (7) in_color_col must be a string
    if not isinstance(in_color_col,str):
        raise Exception("in_color_col must be a string")

    # (8) in_color_col must be a column in in_df
    if not in_color_col in in_df.columns:
        raise Exception("in_color_col must be a column in in_df")

    # (9) in_color_col's column in in_df needs to be string, int64, or float64
    if not (in_df[in_color_col].dtype == 'string[python]' or in_df[in_color_col].dtype == 'int64' or in_df[in_color_col].dtype == 'float64'):
        raise Exception("in_color_col's column in in_df needs to be string, int64, or float64")

    # (10) in_color_col's column in in_df needs to be fully populated
    if not in_df[in_color_col].count() == len(in_df[in_color_col]):
        raise Exception("in_color_col's column in in_df needs to be fully populated")
    
    # (11) in_fig_title needs to be a string
    if not isinstance(in_fig_title,str):
        raise Exception("in_fig_title needs to be a string")
    
    # (12) in_legend_title needs to be a string
    if not isinstance(in_legend_title,str):
        raise Exception("in_legend_title needs to be a string")
    
    # (13) in_colors can only be provided if in_color_col column is of type string
    if (not in_df[in_color_col].dtype == 'string[python]') and not in_colors == None:
        raise Exception("in_colors can only be provided if in_color_col column is of type string")
    
    # (14) in_colors must be provided if in_color_col column is of type string
    if in_df[in_color_col].dtype == 'string[python]' and in_colors == None:
        raise Exception("in_colors must be provided if in_color_col column is of type string")
    
    # (15) If in_colors is provided, it needs to be a dictionary
    if not in_colors == None:
        if not isinstance(in_colors,dict):
            raise Exception("If in_colors is provided, it needs to be a dictionary")
    
    # (16) If in_colors is provided, its keys need to be a 1-for-1 match with unique entries in the in_color_col column
    if not in_colors == None:
        each_in = True
        for i in in_colors.keys():
            if not i in in_df[in_color_col].unique().tolist():
                each_in = False
        if not (each_in and (len(in_colors.keys()) == len(in_df[in_color_col].unique().tolist()))):
            raise Exception("If in_colors is provided, its keys need to be a 1-for-1 match with unique entries in the in_color_col column")

    # (17) If in_colors is provided, its values need to all be strings
    if not in_colors == None:
        for i in in_colors.keys():
            if not isinstance(in_colors[i],str):
                raise Exception("If in_colors is provided, its values need to all be strings")
              
    # (18) in_colorscale can only be provided if the in_color_col column is int64 or float64
    if (not (in_df[in_color_col].dtype == 'int64' or in_df[in_color_col].dtype == 'float64')) and not in_colorscale == None:
        raise Exception("in_colorscale can only be provided if the in_color_col column is int64 or float64")
    
    # (19) If in_colorscale is provided it needs to be a string
    if not in_colorscale == None:
        if not isinstance(in_colorscale,str):
            raise Exception("If in_colorscale is provided it needs to be a string")

    # (20) in_fig_title_size needs to be an int
    if not isinstance(in_fig_title_size,int):
        raise Exception("in_fig_title_size needs to be an int")

    # (21) If in_variable_rename is provided, it needs to be a dict
    if not in_variable_rename == None:
        if not isinstance(in_variable_rename,dict):
            raise Exception("If in_variable_rename is provided, it needs to be a dict")
        
    # (22) If in_variable_rename is provided, it must have a 1 to 1 mapping between its keys and entries in in_var_cols
    if not in_variable_rename == None:
        all_in = True
        for i in in_variable_rename.keys():
            if not i in in_var_cols:
                all_in = False
        if(not(all_in and (len(in_variable_rename.keys()) == len(in_var_cols)))):
            raise Exception("If in_variable_rename is provided, it must have a 1 to 1 mapping between its keys and entries in in_var_cols")
        
    # (23) If in_variable_rename is provided, all the values need to be strings
    if not in_variable_rename == None:
        for i in in_variable_rename.keys():
            if not isinstance(in_variable_rename[i],str):
                raise Exception("If in_variable_rename is provided, all the values need to be strings")    
            
    # (24) in_variable_name_size needs to be an int
    if not isinstance(in_variable_name_size,int):
        raise Exception("in_variable_name_size needs to be an int")

    # (25) in_tick_label_size needs to be an int
    if not isinstance(in_tick_label_size,int):
        raise Exception("in_tick_label_size needs to be an int")
    
    # (26) in_legend_size needs to be an int
    if not isinstance(in_legend_size,int):
        raise Exception("in_legend_size needs to be an int")
    
    # (27) There must be in_var_cols entries corresponding to string columns for in_str_var_orders to be provided
    string_columns = False
    for i in in_var_cols:
        if in_df[i].dtype == "string[python]":
            string_columns = True
            break
    if (not string_columns) and in_str_var_orders:
        raise Exception("There must be in_var_cols entries corresponding to string columns for in_str_var_orders to be provided")

    # (28) If in_str_var_orders is provided, all keys need to be entries within in_var_cols corresponding to string columns
    if not in_str_var_orders == None:
        for i in in_str_var_orders.keys():
            if not i in in_var_cols:
                raise Exception("If in_str_var_orders is provided, all keys need to be entries within in_var_cols corresponding to string columns")
            if not in_df[i].dtype == "string[python]":
                raise Exception("If in_str_var_orders is provided, all keys need to be entries within in_var_cols corresponding to string columns")

    # (29) If in_str_var_orders is provided, each value must be a list
    if not in_str_var_orders == None:
        for i in in_str_var_orders.keys():
            if not isinstance(in_str_var_orders[i],list):
                raise Exception("If in_str_var_orders is provided, each value must be a list")
    
    # (30) If in_str_var_orders is provided, each list value must include only strings
    if not in_str_var_orders == None:
        for i in in_str_var_orders.keys():
            for j in in_str_var_orders[i]:
                if not isinstance(j,str):
                    raise Exception("If in_str_var_orders is provided, each list value must include only strings")
    
    # (31) If in_str_var_orders is provided, each list must have a 1-to-1 match with unique values from the key's column
    if not in_str_var_orders == None:
        for i in in_str_var_orders.keys():
            if not sorted(in_str_var_orders[i]) == sorted(in_df[i].unique().tolist()):
                raise Exception("If in_str_var_orders is provided, each list must have a 1-to-1 match with unique values from the key's column")
    
    # (32) in_fig_width needs to be an int
    if not isinstance(in_fig_width,int):
        raise Exception("in_fig_width needs to be an int")
    
    # (33) in_fig_height needs to be an int
    if not isinstance(in_fig_height,int):
        raise Exception("in_fig_height needs to be an int")
    #----------------- End Confirm Input Variables --------------

    # Create working versions of key inputs
    wrk_df = in_df.copy()
    wrk_var_cols = copy.deepcopy(in_var_cols)
    wrk_colors = copy.deepcopy(in_colors)
    wrk_variable_rename = copy.deepcopy(in_variable_rename)
    wrk_str_var_orders = copy.deepcopy(in_str_var_orders)

    # Determine whether there are discrete colors
    if wrk_colors:
        discrete_colors = True
    else:
        discrete_colors = False
    
    # Create figure
    out_fig = go.Figure()

    # ====================== Define dimensions =================================
    dimensions_lst = []
    for i in wrk_var_cols:
        if wrk_df[i].dtype == 'string[python]':

            int_map = {}
            map_arbitrarily = True
            if not wrk_str_var_orders == None:
                if i in list(wrk_str_var_orders.keys()):
                    map_arbitrarily = False
            
            if map_arbitrarily:
                iter = 1
                for j in wrk_df[i].unique().tolist():
                    int_map[j] = iter
                    iter = iter + 1
            else:
                iter = 0
                for j in wrk_str_var_orders[i]:
                    int_map[j] = len(wrk_str_var_orders[i]) - iter
                    iter = iter + 1
            
            temp_col_name = "{}_Code_0".format(i)
            iter = 1
            while temp_col_name in list(wrk_df.keys()):
                temp_col_name = "{}_Code_{}".format(i,iter)
                iter = iter + 1

            wrk_df[temp_col_name] = wrk_df[i].map(int_map).copy()

            tickvals_lst = []
            ticktext_lst = []
            for j in int_map.keys():
                ticktext_lst.append(str(j))
                tickvals_lst.append(int_map[j])

            if not wrk_variable_rename == None:
                dimensions_lst.append(dict(label = str(wrk_variable_rename[i]),
                                       values = wrk_df[temp_col_name].copy(),
                                       tickvals = tickvals_lst,
                                       ticktext = ticktext_lst))
            else:
                dimensions_lst.append(dict(label = str(i),
                                       values = wrk_df[temp_col_name].copy(),
                                       tickvals = tickvals_lst,
                                       ticktext = ticktext_lst))
        else:
            if not wrk_variable_rename == None:
                dimensions_lst.append(dict(label = str(wrk_variable_rename[i]), values = wrk_df[i].copy()))
            else:
                dimensions_lst.append(dict(label = str(i), values = wrk_df[i].copy()))
    # ====================== End Define dimensions =============================

    # ======= if discrete_colors, create color column in wrk_df and color scale ==========
    if discrete_colors:
        discrete_color_col_name = "discrete_colors_0"
        iter = 1
        while discrete_color_col_name in list(wrk_df.columns):
            discrete_color_col_name = "discrete_colors_{}".format(iter)
            iter = iter + 1

        color_col_map = {}
        discrete_clr_scale = []
        jump_size = 1.0/(float(len(list(in_colors.keys())))-1.0)
        cur_val = 0.0
        for i in in_colors.keys():
            color_col_map[str(i)] = cur_val
            discrete_clr_scale.append([cur_val,in_colors[i]])
            cur_val = cur_val + jump_size

        wrk_df[discrete_color_col_name] = wrk_df[in_color_col].map(color_col_map).copy()
    #=====================================================================================

    #============= Add Trace ===============================
    if discrete_colors:
        out_fig.add_trace(go.Parcoords(
            line = dict(color = wrk_df[discrete_color_col_name].copy(),
                        colorscale = discrete_clr_scale,
                        showscale = False),
            dimensions = dimensions_lst,
            tickfont = dict(size = in_tick_label_size),
            labelfont = dict(size=in_variable_name_size)))
    else:
        if not in_colorscale == None:
            use_colorscale = in_colorscale
        else:
            use_colorscale = 'Viridis'
        out_fig.add_trace(go.Parcoords(
            line = dict(color = wrk_df[in_color_col].copy(),
                        showscale = True,
                        colorscale = use_colorscale,
                        colorbar = dict(
                            tickfont=dict(size=in_legend_size),
                            title = dict(text = in_legend_title, font = dict(size = in_legend_size)))
                        ),
            dimensions = dimensions_lst,
            tickfont = dict(size = in_tick_label_size),
            labelfont = dict(size=in_variable_name_size)))
    #============ End Add Trace ============================

    # Add Title
    out_fig.update_layout(title = {'text': in_fig_title, 'font': {'size': in_fig_title_size}, 'x': 0.5, 'y':0.97})

    #============ if discrete_colors, add legend ===========
    if discrete_colors:
        for i in in_colors.keys():
            out_fig.add_trace(
                go.Scatter(
                    x = [None],
                    y = [None],
                    mode = 'markers',
                    marker = dict(color = in_colors[i]),
                    name = i,
                    showlegend = True
                )
            )
        out_fig.update_layout(legend = dict(title = in_legend_title, title_font = dict (size = in_legend_size), 
                              font = dict(size = in_legend_size)))
        
        out_fig.update_xaxes(showgrid=False, zeroline = False, showticklabels = False)
        out_fig.update_yaxes(showgrid=False, zeroline = False, showticklabels = False)
        out_fig.update_layout(plot_bgcolor='white')

    #=======================================================
    # Set figure size and margin
    out_fig.update_layout(width = in_fig_width, height = in_fig_height)
    out_fig.update_layout(margin = dict(
        t = 130,
        b = 50,
        l = 50,
        r = 50
    ))

    # Return Figure
    return out_fig