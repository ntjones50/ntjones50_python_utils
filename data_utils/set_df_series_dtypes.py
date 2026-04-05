# **************************************
# Function written by Nathan Jones
# **************************************

#------------ Define Imports -----------
import pandas as pd
from pandas import DataFrame as df
import copy
#---------------------------------------

def set_df_series_dtypes(in_df: df, in_dtypes_dict: dict) -> df:
    '''
    Description:

    This function takes in a Pandas dataframe and dictionary where each key is the name of a column 
    (i.e., series) in the dataframe and each value is the desired data type for that column. For each 
    key value pair in the dictionary, the function sets the corresponding column in the dataframe to 
    the desired data type. Not all columns within the datafame need to be specified in the dictionary and 
    modified. Supported data types for columns after modification are: object, string, boolean, float64, 
    int64, datetime64[ns]. The function returns a new Pandas dataframe with the updated column types.

    Inputs:

        in_df (Pandas DataFrame) =      The source Pandas Dataframe from which columns will be updated by the
                                        the function. Each column name need to be a string.

        in_dtypes_dict (Dictionary) =   An input dictionary where each key is a string and corresponds to a 
                                        column within in_df. Each value is a string and corresponds to the
                                        desired data type for that column. Values can be: object, string, 
                                        boolean, float64, int64, datetime64[ns]. Not every column in in_df
                                        needs to be specified in the dictionary. Those not specified will be
                                        unmodified.
        
    Outputs:

        out_df (Pandas DataFrame)  =   New dataframe consisting of in_df with updated column data types.

    Testing:

        Is all the testing for this function automated with pytest (Y/N): Y
        Path to automated testing file for pytest: /tests/test_set_df_series_dtypes.py
        Non-pytest testing description and result: N/A
    '''

    #------------ Confirm user input datatypes ----------------
    # Make sure in_df is a Pandas DataFrame
    if not isinstance(in_df, df):
        raise Exception("in_df needs to be a Pandas DataFrame")
    
    # Make sure in_dtypes_dict is a dictionary
    if not isinstance(in_dtypes_dict, dict):
        raise Exception("in_dtypes_dict needs to be a dictionary")
    #-----------------------------------------------------------
    
    # Create working copies of inputs
    wrk_df = in_df.copy()
    wrk_dict = copy.deepcopy(in_dtypes_dict)

    #------------ Additional user input confirmation -----------
    # Make sure each key in wrk_dict is a string
    for t_key in wrk_dict.keys():
        if not isinstance(t_key,str):
            raise Exception("All keys in in_dtypes_dict need to be strings")
    
    # Make sure each value in wrk_dict is a string
    for t_key in wrk_dict.keys():
        if not isinstance(wrk_dict[t_key],str):
            raise Exception("All values in in_dtypes_dict need to be strings")

    # Make sure each key in wrk_dict is a column in wrk_df
    for t_key in wrk_dict.keys():
        if not t_key in wrk_df.columns:
            raise Exception("All keys in in_dtypes_dict need to be columns in in_df")
    
    # Make sure each value in wrk_dict is an allowable data type
    allowable_types = ['object', 'string', 'boolean', 'float64', 'int64', 'datetime64[ns]']
    for t_key in wrk_dict.keys():
        if not wrk_dict[t_key] in allowable_types:
            raise Exception("All values in in_dtypes_dict need to be either: object, string, boolean, " \
                            "float64, int64, datetime64[ns]")
    #-----------------------------------------------------------

    # Update wrk_df
    for t_key in wrk_dict.keys():
        if not wrk_dict[t_key] == 'datetime64[ns]':
            wrk_df[t_key] = wrk_df[t_key].astype(wrk_dict[t_key])
        else:
            wrk_df[t_key] = pd.to_datetime(wrk_df[t_key])

    # Return wrk_df
    return wrk_df     
