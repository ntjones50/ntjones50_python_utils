# ***************************************************************
# Function written by Nathan Jones
# Pytest tests for graph_utils/gen_parallel_coords_fig.py

# User input checks passed automated review
# Test # 1 Passed Manual Review
# Test # 2 Passed Manual Review
# Test # 3 Passed Manual Review
# Test # 4 Passed Manual Review
# ***************************************************************

#------------ Define Imports -----------
import pandas as pd
import sys
import os
import pytest
from pathlib import Path
#----------------------------------------

#--------------- Import user defined functions -------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "graph_utils")))
from gen_parallel_coords_fig import gen_parallel_coords_fig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_utils")))
from set_df_series_dtypes import set_df_series_dtypes
#-----------------------------------------------------------

def test_gen_parallel_coords_fig():

    # Define test data
    test_dict = {'int64 1': [1,5,3,6,8],
                 'int64_2': [6,7,3,4,6],
                 'float64 1': [2.2,5.5,6.6,7.7,8.8],
                 'float64_2': [3.4,5.6,7.7,5.5,3.9],
                 'float64_missing': [1,2,None,4,5],
                 'string 1': ['a','b','c','g','d'],
                 'string_2': ['as', 'a d', 'e e', 'f','g'],
                 'string_missing': [7,5,None,3,2],
                 'int32_1': [1,2,3,4,5],
                 'string_3': ['d','g','h','r','g']}
    
    #----------------------------------------- Build test dataframe
    test_df_unformat = pd.DataFrame(test_dict)
    test_datatypes = {'int64 1': 'int64',
                      'int64_2': 'int64',
                      'float64 1': 'float64',
                      'float64_2': 'float64',
                      'float64_missing': 'float64',
                      'string 1': 'string',
                      'string_2': 'string',
                      'string_missing': 'string',
                      'string_3': 'string'}
    test_df = set_df_series_dtypes(test_df_unformat,test_datatypes)
    test_df['int32_1'] = test_df['int32_1'].astype('int32')
    #----------------------------------------------------------------

    #===================== Test User Input Checks =========================
    # (1) in_df must be a Pandas Dataframe 
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = 'apple',
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'int64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "in_df must be a Pandas Dataframe"

    # (2) in_var_cols must be a list
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = 'apple',
                                          in_color_col = 'int64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "in_var_cols must be a list"

    # (3) Each entry in in_var_cols needs to be a string
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1',5,'string_2'],
                                          in_color_col = 'int64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "Each entry in in_var_cols needs to be a string"

    # (4) Each entry in in_var_cols needs to be a column within in_df
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','hat','string_2'],
                                          in_color_col = 'int64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "Each entry in in_var_cols needs to be a column within in_df"

    # (5) Each entry in in_var_cols needs to correspond to a column within in_df that is of type 
    #     string, int64, or float64
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','int32_1','string_2'],
                                          in_color_col = 'int64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "Each entry in in_var_cols needs to correspond to a column within in_df that is of type string, int64, or float64"

    # (6) Each entry in in_var_cols needs to correspond to a column within in_df that is fully populated        
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64_missing','string_2'],
                                          in_color_col = 'int64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "Each entry in in_var_cols needs to correspond to a column within in_df that is fully populated"

    # (7) in_color_col must be a string
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 5,
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "in_color_col must be a string"

    # (8) in_color_col must be a column in in_df
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'apple',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "in_color_col must be a column in in_df"

    # (9) in_color_col's column in in_df needs to be string, int64, or float64
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'int32_1',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "in_color_col's column in in_df needs to be string, int64, or float64"

    # (10) in_color_col's column in in_df needs to be fully populated
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64_missing',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "in_color_col's column in in_df needs to be fully populated"

    # (11) in_fig_title needs to be a string
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64 1',
                                          in_fig_title = 5,
                                          in_legend_title = 'Legend')
    assert str(e.value) == "in_fig_title needs to be a string"

    # (12) in_legend_title needs to be a string
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64 1',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 5)
    assert str(e.value) == "in_legend_title needs to be a string"

    # (13) in_colors can only be provided if in_color_col column is of type string    
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64 1',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colors = {'a':'red','b': 'blue'})
    assert str(e.value) == "in_colors can only be provided if in_color_col column is of type string"

    # (14) in_colors must be provided if in_color_col column is of type string
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'string_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend')
    assert str(e.value) == "in_colors must be provided if in_color_col column is of type string"

    # (15) If in_colors is provided, it needs to be a dictionary
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'string_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colors = 'apple')
    assert str(e.value) == "If in_colors is provided, it needs to be a dictionary"

    # (16) If in_colors is provided, its keys need to be a 1-for-1 match with unique entries in the in_color_col column
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'string_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colors = {'a':'red','b': 'blue'})
    assert str(e.value) == "If in_colors is provided, its keys need to be a 1-for-1 match with unique entries in the in_color_col column"

    # (17) If in_colors is provided, its values need to all be strings
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'string 1',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colors = {'a':2,'b': 'blue', 'c':'pink', 'g':'gold', 'd':'green'})
    assert str(e.value) == "If in_colors is provided, its values need to all be strings"

    # (18) in_colorscale can only be provided if the in_color_col column is int64 or float64
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'string 1',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_colors = {'a':'red','b': 'blue', 'c':'pink', 'g':'gold', 'd':'green'})
    assert str(e.value) == "in_colorscale can only be provided if the in_color_col column is int64 or float64"

    # (19) If in_colorscale is provided it needs to be a string
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 4)
    assert str(e.value) == "If in_colorscale is provided it needs to be a string"

    # (20) in_fig_title_size needs to be an int
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_fig_title_size = '5')
    assert str(e.value) == "in_fig_title_size needs to be an int"

    # (21) If in_variable_rename is provided, it needs to be a dict
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_rename = 5)
    assert str(e.value) == "If in_variable_rename is provided, it needs to be a dict"

    # (22) If in_variable_rename is provided, it must have a 1 to 1 mapping between its keys and entries in in_var_cols
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_rename = {'int64 2':'v1','float64 1':'v2','string_2':'v3'})
    assert str(e.value) == "If in_variable_rename is provided, it must have a 1 to 1 mapping between its keys and entries in in_var_cols"

    # (23) If in_variable_rename is provided, all the values need to be strings
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_rename = {'int64 1':5,'float64 1':'v2','string_2':'v3'})
    assert str(e.value) == "If in_variable_rename is provided, all the values need to be strings"

    # (24) in_variable_name_size needs to be an int
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_rename = {'int64 1':'v1','float64 1':'v2','string_2':'v3'},
                                          in_variable_name_size = '5')
    assert str(e.value) == "in_variable_name_size needs to be an int"

    # (25) in_tick_label_size needs to be an int
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_rename = {'int64 1':'v1','float64 1':'v2','string_2':'v3'},
                                          in_variable_name_size = 5,
                                          in_tick_label_size = '5')
    assert str(e.value) == "in_tick_label_size needs to be an int"

    # (26) in_legend_size needs to be an int
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_2'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_rename = {'int64 1':'v1','float64 1':'v2','string_2':'v3'},
                                          in_variable_name_size = 5,
                                          in_legend_size = '5')
    assert str(e.value) == "in_legend_size needs to be an int"

    # (27) There must be in_var_cols entries corresponding to string columns for in_str_var_orders to be provided
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_name_size = 5,
                                          in_str_var_orders = {'int64 1':[1,5,3,6,8]})
    assert str(e.value) == "There must be in_var_cols entries corresponding to string columns for in_str_var_orders to be provided"

    # (28) If in_str_var_orders is provided, all keys need to be entries within in_var_cols corresponding to string columns
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_3'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_name_size = 5,
                                          in_str_var_orders = {'float64 1':['d','g','h','r','g']})
    assert str(e.value) == "If in_str_var_orders is provided, all keys need to be entries within in_var_cols corresponding to string columns"

    # (29) If in_str_var_orders is provided, each value must be a list
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_3'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_name_size = 5,
                                          in_str_var_orders = {'string_3':4})
    assert str(e.value) == "If in_str_var_orders is provided, each value must be a list"

    # (30) If in_str_var_orders is provided, each list value must include only strings
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_3'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_name_size = 5,
                                          in_str_var_orders = {'string_3':[6,'g','h','r','g']})
    assert str(e.value) == "If in_str_var_orders is provided, each list value must include only strings"

    # (31) If in_str_var_orders is provided, each list must have a 1-to-1 match with unique values from the key's column
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_3'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_name_size = 5,
                                          in_str_var_orders = {'string_3':['d','u','h','r','g']})
    assert str(e.value) == "If in_str_var_orders is provided, each list must have a 1-to-1 match with unique values from the key's column"

    # (32) in_fig_width needs to be an int
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_3'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_name_size = 5,
                                          in_fig_width = '5')
    assert str(e.value) == "in_fig_width needs to be an int"

    # (33) in_fig_height needs to be an int
    with pytest.raises(Exception) as e:
        out_fig = gen_parallel_coords_fig(in_df = test_df.copy(),
                                          in_var_cols = ['int64 1','float64 1','string_3'],
                                          in_color_col = 'float64_2',
                                          in_fig_title = 'Test Title',
                                          in_legend_title = 'Legend',
                                          in_colorscale = 'Viridis',
                                          in_variable_name_size = 5,
                                          in_fig_height = '5')
    assert str(e.value) == "in_fig_height needs to be an int"
    #===================== End Test User Input Checks =====================

    # --------------------------------------- TEST # 1 --------------------------------------------
    test_1_fig = gen_parallel_coords_fig(
                    in_df = test_df.copy(),
                    in_var_cols = ['int64 1','float64 1','string 1','float64_2'],
                    in_color_col = 'int64_2',
                    in_fig_title = 'Test #1 Figure',
                    in_legend_title = 'Test Legend',
                    in_colorscale = 'Rainbow',
                    in_fig_title_size = 50,
                    in_variable_rename = {'int64 1':'c1','float64 1':'c2','string 1':'c3',
                                          'float64_2':'c4'},
                    in_variable_name_size = 28,
                    in_tick_label_size = 20,
                    in_legend_size = 24,
                    in_str_var_orders = {'string 1':['d','b','a','g','c']},
                    in_fig_width  = 1200,
                    in_fig_height = 700)
    
    write_path_test_1 = os.path.join(Path(os.path.dirname(__file__)).parent,'test_products',
                                     'gen_parallel_coords_fig', 'test_1.html')

    test_1_fig.write_html(write_path_test_1)
    #---------------------------------------- End TEST # 1 ----------------------------------------

    # --------------------------------------- TEST # 2 --------------------------------------------
    test_2_fig = gen_parallel_coords_fig(
                    in_df = test_df.copy(),
                    in_var_cols = ['float64 1','int64 1','string 1'],
                    in_color_col = 'string 1',
                    in_fig_title = 'Test Figure',
                    in_legend_title = 'Test Legend',
                    in_colors = {'a':'red','b':'green','c':'orange','g':'blue','d':'purple'})

    write_path_test_2 = os.path.join(Path(os.path.dirname(__file__)).parent,'test_products',
                                     'gen_parallel_coords_fig', 'test_2.html')

    test_2_fig.write_html(write_path_test_2)
    #---------------------------------------- End TEST # 2 ----------------------------------------

    # --------------------------------------- TEST # 3 --------------------------------------------
    test_3_fig = gen_parallel_coords_fig(
                    in_df = test_df.copy(),
                    in_var_cols = ['float64 1','int64 1'],
                    in_color_col = 'float64 1',
                    in_fig_title = 'Title',
                    in_legend_title = 'Legend')
    
    write_path_test_3 = os.path.join(Path(os.path.dirname(__file__)).parent,'test_products',
                                     'gen_parallel_coords_fig', 'test_3.html')

    test_3_fig.write_html(write_path_test_3)
    #---------------------------------------- End TEST # 3 ----------------------------------------

    # --------------------------------------- TEST # 4 --------------------------------------------
    test_4_fig = gen_parallel_coords_fig(
                    in_df = test_df.copy(),
                    in_var_cols = ['string_2', 'string 1'],
                    in_color_col = 'string 1',
                    in_fig_title = 'Title',
                    in_legend_title = 'Legend',
                    in_colors = {'a':'pink','b':'green','c':'red','g':'yellow','d':'orange'},
                    in_str_var_orders = {'string 1':['g','a','b','c','d']})

    write_path_test_4 = os.path.join(Path(os.path.dirname(__file__)).parent,'test_products',
                                     'gen_parallel_coords_fig', 'test_4.html')

    test_4_fig.write_html(write_path_test_4)
    #---------------------------------------- End TEST # 4 ----------------------------------------
