# ***************************************************************
# Function written by Nathan Jones
# Pytest tests for graph_utils/gen_welch_procedure_plots.py


# Manual Testing Results:

# Test 1 Figure 0 passed visual inspection
# Test 1 Figure 1 passed visual inspection
# Test 2 Figure 0 passed visual inspection
# Test 2 Figure 1 passed visual inspection
# ***************************************************************

#------------ Define Imports -----------
import pandas as pd
from pandas import DataFrame as df
import sys
import os
import pytest
import numpy as np
#----------------------------------------

#--------------- Import user defined functions -------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "graph_utils")))
from gen_welch_procedure_plots import gen_welch_procedure_plots

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_utils")))
from set_df_series_dtypes import set_df_series_dtypes
#-----------------------------------------------------------

def test_gen_welch_procedure_plots():

    #------------- Create Test Data -----------------
    test_dict = {
                'rep_col_int64_good' : [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3],
                'rep_col_int64_wrongorder' : [1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3],
                'timestep_col_int64_legit' : [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10],
                'timestep_col_int64_wrongorder' : [1,2,3,4,5,6,7,8,9,9,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10],
                'met_col_float64_good' : [1.2,3.6,7.8,3.3,2.5,-8.7,3.4,2.2,1.8,2.9,3.3,2.5,5.5,2.2,6.6,3.8,3.0,
                                        5.5,3.3,7.7,9.9,1.1,4.5,-2.6,7.8,3.5,2.8,4.4,6.9,10.0],
                'met_col_float64_miss' : [1.2,3.6,7.8,3.3,None,-8.7,3.4,2.2,1.8,2.9,3.3,2.5,5.5,2.2,6.6,3.8,3.0,
                                        5.5,3.3,7.7,9.9,1.1,4.5,-2.6,7.8,3.5,2.8,4.4,6.9,10.0],
                'met_col_int_good' : [1,4,5,3,6,4,3,7,4,3,5,2,3,-7,4,3,2,6,7,5,2,3,4,5,6,7,8,9,3,10],
                'str_col' : ["w","2","4","6","5","7","6","t","r","y","w","y","r","e","w","5","6","e","y","e"
                           "3","e","2","5","3","2","6","3","6","r",'y']
                }
    
    temp_test_df = df(test_dict)

    col_types = {
                'rep_col_int64_good': 'int64',
                'rep_col_int64_wrongorder' : 'int64',
                'timestep_col_int64_legit' : 'int64',
                'timestep_col_int64_wrongorder' : 'int64',
                'met_col_float64_good' : 'float64',
                'met_col_float64_miss' : 'float64',
                'met_col_int_good' : 'int64',
                'str_col' : 'string'
                }
    
    test_df = set_df_series_dtypes(temp_test_df, col_types)
    #------------- End Create Test Data -------------

    # in_df needs to be a DataFrame
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  "Test",
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'met_col_float64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == "in_df needs to be a Pandas DataFrame"

    # rep_col needs to be a string
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 3,
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'met_col_float64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == "rep_col needs to be a string"

    # rep_col needs to be a column within in_df
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = '3',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'met_col_float64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == "rep_col needs to be the name of a column within in_df"

    # The rep_col column within in_df needs to be int64
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'met_col_float64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'met_col_float64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'rep_col within in_df needs to be int64'

    # time_step_col needs to be a string
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 1,
                                  metric_col = 'met_col_float64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'time_step_col needs to be a string'

    # time_step_col needs to be a column in in_df
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = '1',
                                  metric_col = 'met_col_float64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'time_step_col needs to be a column within in_df'

    # The time_step_col in in_df needs to be int64
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'met_col_float64_good',
                                  metric_col = 'met_col_float64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'The time_step_col column in in_df needs to be of type int64'

    # metric_col needs to be a string
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 4,
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'metric_col needs to be a string'

    # metric_col needs to be a column within in_df
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = '4',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'metric_col needs to be a column within in_df'

    # metric_col column in in_df needs to be int64 or float64
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'str_col',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'The metric_col column within in_df needs to be int64 or float64'

    # if metric_col column in in_df is float64 it needs to be fully populated
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'met_col_float64_miss',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'The metric col column within in_df needs to be fully populated'

    # n needs to be an int
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = '3',
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'n needs to be of type int'

    # n needs to be the maximum replication
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 300,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'n needs to be the maximum replication number in in_df'

    # m needs to be an int
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = '10',
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'm needs to be of type int'

    # m needs to be the maximum timestep
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = 5,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'm needs to be the maximum timestep within in_df'

    # time_step_units needs to be a string
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = 6,
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'time_step_units needs to be of type str'

    # units_per_timestep needs to be a float
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = 'Minutes',
                                  units_per_timestep = 5,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'units_per_timestep needs to be a float'

    # first_timestep_units needs to be a float
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = 'Minutes',
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'first_timestep_units needs to be a float'

    # metric_name needs to be a string if provided
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = 'Minutes',
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = 1,
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == 'metric_name needs to be a string if provided'

    # if w is provided it needs to be an int
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = 'Minutes',
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollars",
                                  w = 1.0,
                                  x_axis_units = True)
    assert str(e.value) == 'w needs to be an int if provided'

    # x_axis_units needs to be a boolean
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = 'Minutes',
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollars",
                                  w = 1,
                                  x_axis_units = 1)
    assert str(e.value) == 'x_axis_units needs to be a bool'

    # make sure in_df has the correct number of rows
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'timestep_col_int64_legit',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 10,
                                  m = 10,
                                  time_step_units = 'Minutes',
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollars",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == "m and n don't match with the number of rows in in_df"

    # make sure the replication numbers are correct within in_df
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_wrongorder',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = 'Minutes',
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollars",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == "in_df has the wrong number of rows for replication {}".format(1)

    # make sure the timesteps are correct within in_df
    with pytest.raises(Exception) as e:
        gen_welch_procedure_plots(in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_wrongorder',
                                  metric_col = 'rep_col_int64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  w = 1,
                                  x_axis_units = True)
    assert str(e.value) == "in_df has incorrect timesteps for replication {}".format(1)
    #------------------------ User Input Check Testing Complete -----------------------------

    #------------------------ TEST 1 --------------------------------------------------------
    # Float Metric, default w, x_axis_units False

    # 'rep_col_int64_good' : [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3]
    # 'timestep_col_int64_legit' : [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
    # 'met_col_float64_good' : [1.2,3.6,7.8,3.3,2.5,-8.7,3.4,2.2,1.8,2.9,3.3,2.5,5.5,2.2,6.6,3.8,3.0,
    #                            5.5,3.3,7.7,9.9,1.1,4.5,-2.6,7.8,3.5,2.8,4.4,6.9,10.0]

    fig_1, fig_2, out_lst = gen_welch_procedure_plots(
                                  in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'met_col_float64_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  metric_name = "Dollar Price",
                                  x_axis_units = False)

    # [0] - list of replications
    real_0 = [1,2,3]
    assert real_0 == out_lst[0]

    # [1] - list of timesteps
    real_1 = [1,2,3,4,5,6,7,8,9,10]
    assert real_1 == out_lst[1]

    # [2] - list to hold metric mean over replications by timestep
    real_2 = [4.8,2.4,5.933333333,0.966666667,5.633333333,-0.466666667,3.066666667,4.033333333,4,6.866666667]
    assert np.allclose(np.array(real_2),np.array(out_lst[2]))

    # [3] - w
    assert out_lst[3] == 2

    # [4] - list containing moving average values for the first timestep to the m-w timestep
    real_4 = [4.8, 4.377777778, 3.946666667, 2.893333333, 3.026666667, 2.646666667, 3.253333333, 3.5]
    assert np.allclose(np.array(real_4),np.array(out_lst[4]))

    # [5] - x coordinates for figure at index 0
    real_5 = [1,2,3,4,5,6,7,8,9,10]
    assert real_5 == out_lst[5]

    # [6] - x coordinates for figure at index 1
    real_6 = [1,2,3,4,5,6,7,8]
    assert real_6 == out_lst[6]

    fig_1.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_welch_procedure_plots', 'Test_1_Fig_0.html'))
     
    fig_2.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_welch_procedure_plots', 'Test_1_Fig_1.html'))

    #------------------------ End Test 1 ----------------------------------------------------

    #------------------------ TEST 2 --------------------------------------------------------
    # Int Metric, provided w, x_axis_units True, No metric name provided

    # 'rep_col_int64_good' : [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3]
    # 'timestep_col_int64_legit' : [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
    # 'met_col_int_good' : [1,4,5,3,6,4,3,7,4,3,5,2,3,-7,4,3,2,6,7,5,2,3,4,5,6,7,8,9,3,10]

    fig_1, fig_2, out_lst = gen_welch_procedure_plots(
                                  in_df =  test_df.copy(),
                                  rep_col = 'rep_col_int64_good',
                                  time_step_col = 'timestep_col_int64_legit',
                                  metric_col = 'met_col_int_good',
                                  n = 3,
                                  m = 10,
                                  time_step_units = "Minutes",
                                  units_per_timestep = 5.0,
                                  first_timestep_units = 0.0,
                                  w = 1,
                                  x_axis_units = True)
    
    # [0] - list of replications
    real_0 = [1,2,3]
    assert real_0 == out_lst[0]

    # [1] - list of timesteps
    real_1 = [1,2,3,4,5,6,7,8,9,10]
    assert real_1 == out_lst[1]

     # [2] - list to hold metric mean over replications by timestep
    real_2 = [2.666666667,3,4,0.333333333,5.333333333,4.666666667,4.333333333,7.333333333,4.666666667,6]
    assert np.allclose(np.array(real_2),np.array(out_lst[2]))

    # [3] - w
    assert out_lst[3] == 1

    # [4] - list containing moving average values for the first timestep to the m-w timestep
    real_4 = [2.666666667,3.222222222,2.444444444,3.222222222,3.444444444,4.777777778,5.444444444,5.444444444,6]
    assert np.allclose(np.array(real_4),np.array(out_lst[4]))

    # [5] - x coordinates for figure at index 0
    real_5 = [0,5,10,15,20,25,30,35,40,45]
    assert real_5 == out_lst[5]

    # [6] - x coordinates for figure at index 1
    real_6 = [0,5,10,15,20,25,30,35,40]
    assert real_6 == out_lst[6]

    fig_1.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_welch_procedure_plots', 'Test_2_Fig_0.html'))
     
    fig_2.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_welch_procedure_plots', 'Test_2_Fig_1.html'))

