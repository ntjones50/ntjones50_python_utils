# *****************************************************
# Function written by Nathan Jones
# Pytest tests for data_utils/set_df_series_dtypes.py
# *****************************************************

# Imports
import pandas as pd
from pandas import DataFrame as df
import pytest
import sys
import os
import pandas.testing as pdt

# Import function to test
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data_utils")))
from set_df_series_dtypes import set_df_series_dtypes

def test_set_df_series_dtypes():

    # Define test dataframe
    test_df_dict = {'object_1': ['a',None,'c'],
                    'string 1': ['d',None,'f'],
                    'boolean_1': [True,None,False],
                    'float64_1': [1.1,None,3.3],
                    'int64_1': [1,2,3],
                    'datetime64_ns 1': ['1/1/2025',None, '2/2/2028'],
                    'int32': [1,2,3]}
    test_df = df(test_df_dict)
    for i in test_df.columns:
        test_df[i] = test_df[i].astype('object') # All entries set to objects in test dataframe
    
    # define test dictionary
    test_d = {'object_1': 'object',
              'string 1': 'string',
              'boolean_1': 'boolean',
              'float64_1': 'float64',
              'int64_1': 'int64',
              'datetime64_ns 1': 'datetime64[ns]'}

    # Define solution dataframe
    sol_df = test_df.copy()
    sol_df['object_1'] = sol_df['object_1'].astype('object')
    sol_df['string 1'] = sol_df['string 1'].astype('string')
    sol_df['boolean_1'] = sol_df['boolean_1'].astype('boolean')
    sol_df['float64_1'] = sol_df['float64_1'].astype('float64')
    sol_df['int64_1'] = sol_df['int64_1'].astype('int64')
    sol_df['datetime64_ns 1'] = pd.to_datetime(sol_df['datetime64_ns 1'])

    #---------------------------------
    # Test user input errors

    # in_df Pandas DataFrame
    with pytest.raises(Exception) as e:
        set_df_series_dtypes('hat', {'object_1': 'object'})
    assert str(e.value) == "in_df needs to be a Pandas DataFrame"
    
    # in_dtypes_dict dictionary
    with pytest.raises(Exception) as e:
        set_df_series_dtypes(test_df, 'apple')
    assert str(e.value) == "in_dtypes_dict needs to be a dictionary"

    # dictionary keys are strings
    with pytest.raises(Exception) as e:
        set_df_series_dtypes(test_df, {1: 'object'})
    assert str(e.value) == "All keys in in_dtypes_dict need to be strings"

    # dictionary values are strings
    with pytest.raises(Exception) as e:
        set_df_series_dtypes(test_df, {'object_1': 5})
    assert str(e.value) == "All values in in_dtypes_dict need to be strings"

    # all keys are dataframe columns
    with pytest.raises(Exception) as e:
        set_df_series_dtypes(test_df, {'Cat': 'object'})
    assert str(e.value) == "All keys in in_dtypes_dict need to be columns in in_df"

    # All dictionary values allowable types
    with pytest.raises(Exception) as e:
        set_df_series_dtypes(test_df, {'object_1': 'int32'})
    assert str(e.value) ==  "All values in in_dtypes_dict need to be either: object, string, boolean, " \
                            "float64, int64, datetime64[ns]"
    #---------------------------------

    # Test full output dataframe match
    comp_df = set_df_series_dtypes(test_df, test_d)
    pdt.assert_frame_equal(comp_df, sol_df,
                           check_index_type = True, check_column_type = True,
                           check_exact = True)
    
    # Tests for each column data type
    comp_df_2 = set_df_series_dtypes(test_df, test_d)
    assert comp_df_2['object_1'].dtype == 'object'
    assert comp_df_2['string 1'].dtype == 'string'
    assert comp_df_2['boolean_1'].dtype == 'boolean'
    assert comp_df_2['float64_1'].dtype == 'float64'
    assert comp_df_2['int64_1'].dtype == 'int64'
    assert comp_df_2['datetime64_ns 1'].dtype == 'datetime64[ns]'
    assert comp_df_2['int32'].dtype == 'object'