
from os import listdir
from os.path import isfile, join
import re
from typing import List

import pandas as pd
import numpy as np

import config as cnf


def setup_filepaths(path: str,
                    pattern: str) -> List[str]:
    """
    returns the matching file paths in a list
    
    Params:
    -------
    path : (str) file path where to look for files
    pattern : (str) regex pattern for matching files

    Returns:
    -------
    filepaths : (list of str) list of matching file paths
    """
    filepaths = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    r = re.compile(pattern)
    filepaths = list(filter(r.match, filepaths))
    return filepaths

def compile_df(filepaths: List[str]) -> pd.DataFrame:
    """
    loads data from all file paths and combines them into single dataframe
    assumes all files have same format
    
    Params:
    ------
    filepaths : (list of str) all filepaths to be loaded to df

    Returns:
    -------
    df : (dataframe) containing data from all files
    """
    df = pd.DataFrame()
    for path in filepaths:
        df_tmp = pd.DataFrame()
        df_tmp  = pd.read_csv(path, low_memory=False)
        df = df.append(df_tmp)
    return df

def convert_to_datetime(df: pd.DataFrame,
                        cols: List[str],
                        date_format: str) -> pd.DataFrame:
    """
    converts columns from cols parameter in dataframe to 
    to datetime objects
    assumes all columns have same strftime format

    Params:
    -------
    df : (dataframe) dataframe with columns to be converted
    cols : (list of str) list of columns to be converted
    date_format : (str) strf representation of date format in cols
    """
    for col in cols:
        df[col] = pd.to_datetime(df[col], format=date_format)

    return df

def convert_nans(df: pd.DataFrame,
                 cols: List[str],
                 replace_value:str) -> pd.DataFrame:
    """
    convert nan-values to defined state

    Params:
    -------
    df : (dataframe) dataframe with columns for which to replace nan values
    cols : (list of str) columns to be converted
    replace_value : (str) value to replace nans
    
    Returns:
    -------
    df : (dataframe) with converted columns
    """
    for col in cols:
        df[col].replace(np.nan, replace_value, inplace=True)
    return df


if __name__ == "__main__":
    # loading data
    fps = setup_filepaths(cnf.PATH,
                          cnf.FILENAME_PATTERN)

    df = compile_df(fps)

    # data preprocessing
    df = convert_to_datetime(df, cnf.DATE_COLS,
                             cnf.DATE_FORMAT)
    df = convert_nans(df, cnf.YN_COLS,
                      cnf.YN_REPL_VAL)

    print(df['DIED'].unique())
