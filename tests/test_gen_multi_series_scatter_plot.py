# ***************************************************************
# Function written by Nathan Jones
# Pytest tests for graph_utils/gen_multi_series_scatter_plot.py

# Pytest fully passed. Generated charts for the 9 
# tests all passed manual inspection
# ***************************************************************

#------------ Define Imports -----------
import pandas as pd
from pandas import DataFrame as df
import sys
import os
import pytest
#----------------------------------------

#--------------- Import user defined functions -------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "graph_utils")))
from gen_multi_series_scatter_plot import gen_multi_series_scatter_plot

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_utils")))
from set_df_series_dtypes import set_df_series_dtypes

#-----------------------------------------------------------

def test_gen_multi_series_scatter_plot():

    #------------------ Create Test Data ------------------
    test_dict = {'series_str_multi': ['dog','dog','dog','2','2','2'],
                 'series_str_single': ['1','1','1','1','1','1'],
                 'series_missing': ['1','1',None,'1','1','1'],
                 'x_data_int64': [-1,-2,3,4,5,6],
                 'x data float64': [-1.5,-2.5,3.5,4.5,5.5,6.5],
                 'x_data_float64_missing': [1.5,None,3.5,4.5,5.5,6.5],
                 'y_data_int64': [-6,-4,-1,0,1,2],
                 'y data float64': [-6.5,-4.5,-1.5,0.5,1.5,2.5],
                 'y_data_float64_missing': [-6.5,None,-1.5,0.5,1.5,2.5],
                 'data_int32': [1,2,3,4,5,6]}
    
    temp_df = df(test_dict)

    col_types = {'series_str_multi': 'string',
                 'series_str_single': 'string',
                 'series_missing': 'string',
                 'x_data_int64': 'int64',
                 'x data float64': 'float64',
                 'x_data_float64_missing': 'float64',
                 'y_data_int64': 'int64',
                 'y data float64': 'float64',
                 'y_data_float64_missing': 'float64',
                 'data_int32': 'int64'}
    
    test_df = set_df_series_dtypes(temp_df,col_types)
    test_df['data_int32'] = test_df['data_int32'] .astype('int32')
    #------------------ End Create Test Data ------------------

    #------------------ Test User Input Exceptions -----------

    # Ensure in_df is a DataFrame
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = 'dog', series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "in_df needs to be a Pandas DataFrame"

    # Ensure series_col is a string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 1,
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "series_col needs to be a string"

    # Ensure series_col is a series in in_df
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "series_col needs to be a column in in_df"

    # Ensure series_col in in_df is string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'x data float64',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == 'series_col in in_df needs to be of type string'

    # Ensure series_col is fully populate in in_df
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_missing',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "series_col within in_df needs to be fully populated"

    # Ensure x_data_col is a string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 1, y_data_col = 'y data float64',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "x_data_col needs to be a string"

    # Ensure x_data_col is a column in in_df
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data', y_data_col = 'y data float64',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "x_data_col needs to be a column in in_df"

    # Ensure x_data_col in in_df is of type int64 or float64
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'data_int32', y_data_col = 'y data float64',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == 'x_data_col in in_df needs to be of type int64 or float64'

    # Ensure x_data_col is fully populate in in_df
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x_data_float64_missing', y_data_col = 'y data float64',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "x_data_col within in_df needs to be fully populated"

    # Ensure y_data_col is a string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 1,
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "y_data_col needs to be a string"

    # Ensure y_data_col is a column in in_df
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = '1',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "y_data_col needs to be a column in in_df"

    # Ensure y_data_col in in_df is of type int64 or float64
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'data_int32',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == 'y_data_col in in_df needs to be of type int64 or float64'

    # Ensure y_data_col is fully populate in in_df
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y_data_float64_missing',
                                      title = 'Test Title', x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "y_data_col within in_df needs to be fully populated"

    # Ensure title is a string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = 1, x_axis_label = 'X-Axis Lab',
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "Title needs to be a string"
    
    # Ensure x_axis_label is a string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = 1,
                                      y_axis_label = 'Y-Axis Lab', legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "x_axis_label needs to be a string"

    # Ensure y_axis_label is a string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = 1, legend_label = 'Legend Lab',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "y_axis_label needs to be a string"

    # Ensure legend_label is a string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = 4,
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "legend_label needs to be a string"

    # If provided, ensure x_axis_range is a list
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = '[-10.0,10.0]', y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "x_axis_range needs to be a list"

    # If provided, ensure y_axis_range is a list
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = '[-10.0,10.0]',
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "y_axis_range needs to be a list"
    
    # If provided, ensure, x_axis range has two entries 
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "x_axis_range must have 2 entries"

    # If provided, ensure, y_axis range has two entries 
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "y_axis_range must have 2 entries"

    # If provided, ensure, x_axis range entry types match x_data_col
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10,10], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "x_axis_range values must be of comparable type to the in_df x_data_col"
    
    # If provided, ensure, y_axis range entry types match y_data_col
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10,10],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == "y_axis_range values must be of comparable type to the in_df y_data_col"

    # If provided, ensure all x_data_col values are within the range of x_axis_range exclusive of bounds
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-2.5,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == 'All values in the x_data_col of in_df must be within the bounds of x_axis_range exclusive of the bounds'
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,6.5], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == 'All values in the x_data_col of in_df must be within the bounds of x_axis_range exclusive of the bounds'

    # If provided, ensure all y_data_col values are within the range of y_axis_range exclusive of bounds
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-6.5,10.0],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == 'All values in the y_data_col of in_df must be within the bounds of y_axis_range exclusive of the bounds'
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,2.5],
                                      color_dict = {'dog':'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == 'All values in the y_data_col of in_df must be within the bounds of y_axis_range exclusive of the bounds'

    # If provided, ensure color_dict is a dictionary
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = "{'dog':'blue', '2': 'green'}", pt_size = 20)
    assert str(e.value) == 'color_dict must be a dictionary'

    # If provided, ensure each key in color_dict is a string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {1:'blue', '2': 'green'}, pt_size = 20)
    assert str(e.value) == 'All keys in color_dict must be strings'

    # If provided, ensure each value in color_dict is a string
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog':5, '2': 'green'}, pt_size = 20)
    assert str(e.value) == 'All values in color_dict must be strings'

    # If provided, make sure each key in color_dict is a series in series_col and all series in 
    # series_col are accounted for
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog': '5'}, pt_size = 20)
    assert str(e.value) == 'All series need to be accounted for in color_dict'
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog': '5', '3': 'h'}, pt_size = 20)
    assert str(e.value) == 'All keys in color_dict need to be series in the series_col column'

    # Ensure pt_size is an int if provided
    with pytest.raises(Exception) as e:
        gen_multi_series_scatter_plot(in_df = test_df, series_col = 'series_str_multi',
                                      x_data_col = 'x data float64', y_data_col = 'y data float64',
                                      title = '1', x_axis_label = '1',
                                      y_axis_label = '1', legend_label = '4',
                                      x_axis_range = [-10.0,10.0], y_axis_range = [-10.0,10.0],
                                      color_dict = {'dog': '5', '2': 'h'}, pt_size = '20')
    assert str(e.value) == "pt_size needs to be an int"
    #----------------- End Test User Input Exceptions ---------

    #---------------------- Test 1 -----------------------------
    # 'series_str_multi': ['dog','dog','dog','2','2','2']
    # 'x data float64': [-1.5,-2.5,3.5,4.5,5.5,6.5]
    # 'y data float64': [-6.5,-4.5,-1.5,0.5,1.5,2.5]
    fig = gen_multi_series_scatter_plot(in_df = test_df,
                                        series_col = 'series_str_multi',
                                        x_data_col = 'x data float64',
                                        y_data_col = 'y data float64',
                                        title = 'Test Title',
                                        x_axis_label = 'X-Axis Lab',
                                        y_axis_label = 'Y-Axis Lab',
                                        legend_label = 'Legend Lab',
                                        x_axis_range = [-10.0,10.0],
                                        y_axis_range = [-10.0,10.0],
                                        color_dict = {'dog':'blue', '2': 'green'},
                                        pt_size = 35)

    fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_multi_series_scatter_plot', 'Test_1.html'))
    #--------------------- End Test 1--------------------------

    #---------------------- Test 2 -----------------------------
    # 'series_str_multi': ['dog','dog','dog','2','2','2']
    # 'x data float64': [-1.5,-2.5,3.5,4.5,5.5,6.5]
    # 'y_data_int64': [-6,-4,-1,0,1,2]
    fig = gen_multi_series_scatter_plot(in_df = test_df,
                                        series_col = 'series_str_multi',
                                        x_data_col = 'x data float64',
                                        y_data_col = 'y_data_int64',
                                        title = 'Test Title',
                                        x_axis_label = 'X-Axis Lab',
                                        y_axis_label = 'Y-Axis Lab',
                                        legend_label = 'Legend Lab')

    fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_multi_series_scatter_plot', 'Test_2.html'))
    #--------------------- End Test 2--------------------------

    #---------------------- Test 3 -----------------------------
    # 'series_str_multi': ['dog','dog','dog','2','2','2']
    # 'x_data_int64': [-1,-2,3,4,5,6]
    # 'y data float64': [-6.5,-4.5,-1.5,0.5,1.5,2.5]
    fig = gen_multi_series_scatter_plot(in_df = test_df,
                                        series_col = 'series_str_multi',
                                        x_data_col = 'x_data_int64',
                                        y_data_col = 'y data float64',
                                        title = 'Test Title',
                                        x_axis_label = 'X-Axis Lab',
                                        y_axis_label = 'Y-Axis Lab',
                                        legend_label = 'Legend Lab',
                                        x_axis_range = [-10,10],
                                        y_axis_range = [-10.0,10.0],
                                        color_dict = {'dog':'red', '2': 'blue'},
                                        pt_size = 50)

    fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_multi_series_scatter_plot', 'Test_3.html'))
    #--------------------- End Test 3--------------------------

    #---------------------- Test 4 -----------------------------
    # 'series_str_multi': ['dog','dog','dog','2','2','2']
    # 'x_data_int64': [-1,-2,3,4,5,6]
    # 'y_data_int64': [-6,-4,-1,0,1,2]
    fig = gen_multi_series_scatter_plot(in_df = test_df,
                                        series_col = 'series_str_multi',
                                        x_data_col = 'x_data_int64',
                                        y_data_col =  'y_data_int64',
                                        title = 'Test Title',
                                        x_axis_label = 'X-Axis Lab',
                                        y_axis_label = 'Y-Axis Lab',
                                        legend_label = 'Legend Lab',
                                        color_dict = {'dog':'blue', '2': 'green'})

    fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_multi_series_scatter_plot', 'Test_4.html'))
    #--------------------- End Test 4--------------------------

    #---------------------- Test 5 -----------------------------
    # 'series_str_single': ['1','1','1','1','1','1']
    # 'x data float64': [-1.5,-2.5,3.5,4.5,5.5,6.5]
    # 'y data float64': [-6.5,-4.5,-1.5,0.5,1.5,2.5]
    fig = gen_multi_series_scatter_plot(in_df = test_df,
                                        series_col = 'series_str_single',
                                        x_data_col = 'x data float64',
                                        y_data_col = 'y data float64',
                                        title = 'Test Title',
                                        x_axis_label = 'X-Axis Lab',
                                        y_axis_label = 'Y-Axis Lab',
                                        legend_label = 'Legend Lab',
                                        x_axis_range = [-10.0,10.0],
                                        y_axis_range = [-10.0,10.0],
                                        color_dict = {'1':'blue'},
                                        pt_size = 35)

    fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_multi_series_scatter_plot', 'Test_5.html'))
    #--------------------- End Test 5--------------------------

    #---------------------- Test 6 -----------------------------
    # 'series_str_single': ['1','1','1','1','1','1']
    # 'x data float64': [-1.5,-2.5,3.5,4.5,5.5,6.5]
    # 'y_data_int64': [-6,-4,-1,0,1,2]
    fig = gen_multi_series_scatter_plot(in_df = test_df,
                                        series_col = 'series_str_single',
                                        x_data_col = 'x data float64',
                                        y_data_col = 'y_data_int64',
                                        title = 'Test Title',
                                        x_axis_label = 'X-Axis Lab',
                                        y_axis_label = 'Y-Axis Lab',
                                        legend_label = 'Legend Lab')

    fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_multi_series_scatter_plot', 'Test_6.html'))
    #--------------------- End Test 6--------------------------

    #---------------------- Test 7 -----------------------------
    # 'series_str_single': ['1','1','1','1','1','1']
    # 'x_data_int64': [-1,-2,3,4,5,6]
    # 'y data float64': [-6.5,-4.5,-1.5,0.5,1.5,2.5]
    fig = gen_multi_series_scatter_plot(in_df = test_df,
                                        series_col = 'series_str_single',
                                        x_data_col = 'x_data_int64',
                                        y_data_col = 'y data float64',
                                        title = 'Test Title',
                                        x_axis_label = 'X-Axis Lab',
                                        y_axis_label = 'Y-Axis Lab',
                                        legend_label = 'Legend Lab',
                                        x_axis_range = [-10,10],
                                        y_axis_range = [-10.0,10.0],
                                        color_dict = {'1':'red'},
                                        pt_size = 50)

    fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_multi_series_scatter_plot', 'Test_7.html'))
    #--------------------- End Test 7--------------------------

    #---------------------- Test 8 -----------------------------
    # 'series_str_single': ['1','1','1','1','1','1']
    # 'x_data_int64': [-1,-2,3,4,5,6]
    # 'y_data_int64': [-6,-4,-1,0,1,2]
    fig = gen_multi_series_scatter_plot(in_df = test_df,
                                        series_col = 'series_str_single',
                                        x_data_col = 'x_data_int64',
                                        y_data_col =  'y_data_int64',
                                        title = 'Test Title',
                                        x_axis_label = 'X-Axis Lab',
                                        y_axis_label = 'Y-Axis Lab',
                                        legend_label = 'Legend Lab',
                                        color_dict = {'1':'blue'})

    fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_multi_series_scatter_plot', 'Test_8.html'))
    #--------------------- End Test 8--------------------------

    #---------------------- Test 9 -----------------------------
    # 'series_str_single': ['1','1','1','1','1','1']
    # 'x_data_int64': [-1,-2,3,4,5,6]
    # 'y_data_int64': [-6,-4,-1,0,1,2]
    fig = gen_multi_series_scatter_plot(in_df = test_df,
                                        series_col = 'series_str_single',
                                        x_data_col = 'x_data_int64',
                                        y_data_col =  'y_data_int64',
                                        title = 'Test Title',
                                        x_axis_label = 'X-Axis Lab',
                                        y_axis_label = 'Y-Axis Lab',
                                        legend_label = 'Legend Lab',
                                        x_axis_range = [-10,10],
                                        y_axis_range = [-20,20],
                                        color_dict = {'1':'blue'})

    fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_multi_series_scatter_plot', 'Test_9.html'))
    #--------------------- End Test 9--------------------------
