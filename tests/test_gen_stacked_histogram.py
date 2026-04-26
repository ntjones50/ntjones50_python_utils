# **************************************
# File written by Nathan Jones

# On 4/26/2026, function initially passed input check testing via automated pytest testing

# On 4/26/2026, function deemed to have passed Test # 1 through automated pytest testing and
# manual inspection of figure.

# On 4/26/2026, function passed Test # 2 through automated pytest testing and
# manual inspection of figure.

# On 4/26/2026, function passed Test # 3 through automated pytest testing and
# manual inspection of figure.
# **************************************

#------------ Define Imports -----------
import pandas as pd
import sys
import os
import pytest
#----------------------------------------

#--------------- Import user defined function -------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "graph_utils")))
from gen_stacked_histogram import gen_stacked_histogram
#----------------------------------------------------------

def test_gen_stacked_histogram():

    # -------------------- Generate Testing Dataset 1 ---------------------------
    test_df_1 = pd.DataFrame({
        'float64_1': [0.0,1.0,2.0,5.0,5.5,6.0,6.0,9.0,9.8,10.0],
        'float64_2': [-5.5,-6.5,-4.2,0.0,4.56,2.74,9.0,10.0,8.2,6.5],
        'float64_3': [0.0, 2.0, 3.0, 5.0, 6.0, 6.5, 6.7, 7.0, 8.0, 10.0],
        'string_same': ['1','1','1','1','1','1','1','1','1','1'],
        'string_diff': ['1','2','1','2','1','2','1','2','1','2'],
        'int64_1':[1,1,1,1,1,1,1,1,1,1],
        'float64_missing': [1.1,1.1,1.1,1.1,1.1,None,1.1,1.1,1.1,1.1],
        'string_missing':['1','1','1','1','1','1',None,'1','1','1']})

    test_df_1_dtypes = {
        'float64_1': 'float64',
        'float64_2': 'float64',
        'float64_3': 'float64',
        'string_same': 'string',
        'string_diff': 'string',
        'int64_1': 'int64',
        'float64_missing': 'float64',
        'string_missing': 'string'}

    for i in test_df_1_dtypes.keys():
        test_df_1[i] = test_df_1[i].astype(test_df_1_dtypes[i])
    #--------------------- End Generate Testing Dataset 1 -----------------------

    #------------------- Generate Testing Dataset 2 -----------------------------
    test_df_2 = pd.DataFrame({
        'float64_1':[-1.123456,0.5,3.567897],
        'string_1': ['1','1','1']})
    
    test_df_2_dtypes = {'float64_1':'float64',
                        'string_1':'string'}
    
    for i in test_df_2.dtypes.keys():
        test_df_2[i] = test_df_2[i].astype(test_df_2_dtypes[i])
    #--------------------- End Generate Testing Dataset 2 -----------------------

    #--------------------- Test Input Checks -----------------------
    # (1) df must be a Pandas DataFrame
    with pytest.raises(TypeError) as e:
        gen_stacked_histogram(
            df = 'D',
            data_col = 'float64_1',
            series_col = 'string_same',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label')
    assert str(e.value) == "(1) df must be a Pandas DataFrame"

    # (2) data_col needs to be a column in df
    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1_1',
            series_col = 'string_same',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label')
    assert str(e.value) == "(2) data_col needs to be a column in df"

    # (3) data_col column within df needs to be of type float64
    with pytest.raises(TypeError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'int64_1',
            series_col = 'string_same',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label')
    assert str(e.value) == "(3) data_col column within df needs to be of type float64"

    # (4) data_col column within df needs to be fully populated
    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_missing',
            series_col = 'string_same',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label')
    assert str(e.value) == "(4) data_col column within df needs to be fully populated"

    # (5) series_col needs to be a column in df
    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_same_1',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label')
    assert str(e.value) == "(5) series_col needs to be a column in df"

    # (6) series_col column within df needs to be of type string
    with pytest.raises(TypeError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'float64_1',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label')
    assert str(e.value) == "(6) series_col column within df needs to be of type string"

    # (7) series_col column within df needs to be fully populated
    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_missing',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label')
    assert str(e.value) == "(7) series_col column within df needs to be fully populated"

    # (8) There needs to be a 1-to-1 match between entries in series_stacking and unique values
    #     in the series_col column of df
    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_same',
            series_stacking = ['9'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label')
    assert str(e.value) == ("(8) There needs to be a 1-to-1 match between entries in series_stacking " 
                            "and unique values in the series_col column of df")

    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_same',
            series_stacking = ['1','1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label')
    assert str(e.value) == ("(8) There needs to be a 1-to-1 match between entries in series_stacking " 
                            "and unique values in the series_col column of df")

    # (9) If color_dict is included, there needs to be a 1-to-1 match between its keys and entries
    #     in series_stacking
    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_same',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label',
            color_dict = {'9':'blue'})
    assert str(e.value) == ("(9) If color_dict is included, there needs to be a 1-to-1 match " 
                              "between its keys and entries in series_stacking")

    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_same',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label',
            color_dict = {'1':'blue','2':'red'})
    assert str(e.value) == ("(9) If color_dict is included, there needs to be a 1-to-1 match " 
                              "between its keys and entries in series_stacking")

    # (10) hover_val_decimal_places can only be set if frequency = False
    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_same',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label',
            hover_val_decimal_places = 5,
            frequency = True)
    assert str(e.value) == "(10) hover_val_decimal_places can only be set if frequency = False"

    # (11) If hover_bin_decimal_places is set, value must be >= 1
    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_same',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label',
            hover_bin_decimal_places = 0,
            frequency = True)
    assert str(e.value) == "(11) If hover_bin_decimal_places is set, value must be >= 1"

    # (12) If hover_val_decimal_places is set, value must be >= 1
    with pytest.raises(ValueError) as e:
        gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_same',
            series_stacking = ['1'],
            title = 'Title',
            x_axis_label = 'X Label',
            y_axis_label = 'Y Label',
            legend_label = 'Legend Label',
            hover_val_decimal_places = 0,
            frequency = False)
    assert str(e.value) == "(12) If hover_val_decimal_places is set, value must be >= 1"
    #--------------------- End Test Input Checks --------------------

    #--------------------- Test # 1 ---------------------------------
    test_1_fig, test_1_lst = gen_stacked_histogram(
            df = test_df_1,
            data_col = 'float64_1',
            series_col = 'string_diff',
            series_stacking = ['1','2'],
            title = 'Test # 1 Figure',
            x_axis_label = 'Values',
            y_axis_label = 'Bin Frequency',
            legend_label = 'Test Legend',
            bin_count = 10,
            frequency = True,
            title_size = 35,
            x_axis_label_size = 30,
            y_axis_label_size = 30,
            legend_label_size = 30,
            legend_text_size = 25,
            x_axis_tick_label_size = 22,
            y_axis_tick_label_size = 22,
            color_dict = {'1':'blue', '2':'green'},
            fig_width = 1150,
            fig_height = 650,
            hover_bin_decimal_places = 4,
            x_axis_tick_label_standoff = 15,
            y_axis_tick_label_standoff = 15)

    # Test number of bins
    assert test_1_lst[0] == 10

    # Test bin boundaries for each series
    bin_boundary_answers_1 = {'1':[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0],
                              '2':[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]}
    assert bin_boundary_answers_1 == test_1_lst[1]

    # Test bin heights for each series
    bin_heights_answer_1 = {'1':[1,0,1,0,0,1,1,0,0,1],
                            '2':[0,1,0,0,0,1,1,0,0,2]}
    assert bin_heights_answer_1 == test_1_lst[2]

    # Test bin hover test
    bin_hovers_answers_1 = {'1': ["1: bin [0.0,1.0) -> Freq. = 1",
                                  "1: bin [1.0,2.0) -> Freq. = 0",
                                  "1: bin [2.0,3.0) -> Freq. = 1",
                                  "1: bin [3.0,4.0) -> Freq. = 0",
                                  "1: bin [4.0,5.0) -> Freq. = 0",
                                  "1: bin [5.0,6.0) -> Freq. = 1",
                                  "1: bin [6.0,7.0) -> Freq. = 1",
                                  "1: bin [7.0,8.0) -> Freq. = 0",
                                  "1: bin [8.0,9.0) -> Freq. = 0",
                                  "1: bin [9.0,10.0] -> Freq. = 1"],
                            '2': ["2: bin [0.0,1.0) -> Freq. = 0",
                                  "2: bin [1.0,2.0) -> Freq. = 1",
                                  "2: bin [2.0,3.0) -> Freq. = 0",
                                  "2: bin [3.0,4.0) -> Freq. = 0",
                                  "2: bin [4.0,5.0) -> Freq. = 0",
                                  "2: bin [5.0,6.0) -> Freq. = 1",
                                  "2: bin [6.0,7.0) -> Freq. = 1",
                                  "2: bin [7.0,8.0) -> Freq. = 0",
                                  "2: bin [8.0,9.0) -> Freq. = 0",
                                  "2: bin [9.0,10.0] -> Freq. = 2"]}
    assert bin_hovers_answers_1 == test_1_lst[3]

    # Write figure to file
    test_1_fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_stacked_histogram', 'Test_1_Fig.html'))
    #--------------------- End Test # 1 -----------------------------

    #--------------------- Test # 2 ---------------------------------
    test_2_fig, test_2_lst = gen_stacked_histogram(
        df = test_df_1.copy(),
        data_col = 'float64_2',
        series_col = 'string_same',
        series_stacking = ['1'],
        title = 'Test Title',
        x_axis_label = 'Test X',
        y_axis_label = 'Test Y',
        legend_label = 'Test Legend',
        frequency = False,
        hover_val_decimal_places = 1)
    
    # Test # of bins
    assert test_2_lst[0] == 4

    # Test bin boundaries for each series
    bin_boundary_answers_2 = {'1':[-6.5, -2.375, 1.75, 5.875, 10.0]}
    assert bin_boundary_answers_2 == test_2_lst[1]

    # Test bin heights for each series
    bin_heights_answer_2 = {'1':[0.3,0.1,0.2,0.4]}
    assert bin_heights_answer_2 == test_2_lst[2]

    # Test bin hover test
    bin_hovers_answers_2 = {'1': ["1: bin [-6.5,-2.375) -> Relative Freq. = 0.3",
                                  "1: bin [-2.375,1.75) -> Relative Freq. = 0.1",
                                  "1: bin [1.75,5.875) -> Relative Freq. = 0.2",
                                  "1: bin [5.875,10.0] -> Relative Freq. = 0.4"]}
    assert bin_hovers_answers_2 == test_2_lst[3]


    # Write figure to file
    test_2_fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_stacked_histogram', 'Test_2_Fig.html'))
    #--------------------- End Test # 2 -----------------------------

    #--------------------- Test # 3 ---------------------------------
    test_3_fig, test_3_lst = gen_stacked_histogram(
        df = test_df_2.copy(),
        data_col = 'float64_1',
        series_col = 'string_1',
        series_stacking = ['1'],
        title = 'Test Title',
        x_axis_label = 'Test X',
        y_axis_label = 'Test Y',
        legend_label = 'Test Legend',
        frequency = False,
        hover_val_decimal_places = 4,
        hover_bin_decimal_places = 4,
        bin_count = 2)
    
    # Test # of bins
    assert test_3_lst[0] == 2

    # Test bin boundaries for each series
    bin_boundary_answers_3 = {'1':[-1.123456, float((3.567897 + 1.123456)/2 -1.123456), 3.567897]}
    assert bin_boundary_answers_3 == test_3_lst[1]

    # Test bin heights for each series
    bin_heights_answer_3 = {'1':[2.0/3.0,1.0/3.0]}
    assert bin_heights_answer_3 == test_3_lst[2]

    # Test bin hover test
    bin_hovers_answers_3 = {'1': ["1: bin [-1.1235,1.2222) -> Relative Freq. = 0.6667",
                                  "1: bin [1.2222,3.5679] -> Relative Freq. = 0.3333"]}
    assert bin_hovers_answers_3 == test_3_lst[3]

    # Write figure to file
    test_3_fig.write_html(os.path.join(os.path.dirname(__file__), '..','test_products',
                                'gen_stacked_histogram', 'Test_3_Fig.html'))
    #--------------------- End Test # 3 -----------------------------
