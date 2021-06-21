
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

def create_binning(df: pd.DataFrame,
                   col_src: str,
                   col_tgt: str,
                   cut_bins: List[int],
                   labels: List[str]) -> pd.DataFrame:
    """
    creates binning for colum

    Params:
    -------
    df : (dataframe) data with column to be binned
    col_src : (str) column to be binned
    col_tgt : (str) column to store binning results
    cut_bins : (list of int) list values at which to cut_bins
    labels : (list of str) labels to be used for bins

    Returns:
    --------
    df : (dataframe) dataframe including converted bins
    """
    if labels == None:
        df[col_tgt] = pd.cut(df[col_src], bins=cut_bins)
    else:
        df[col_tgt] = pd.cut(df[col_src],
                             bins=cut_bins,
                             labels=labels)

    return df
        

def get_all_vaers_data(path: List[str] = cnf.PATH,
                       pattern: str = cnf.FILENAME_PATTERN,
                       dt_cols: List[str] = cnf.DATE_COLS,
                       dt_format: str = cnf.DATE_FORMAT,
                       nan_cols: List[str] = cnf.YN_COLS,
                       nan_repl_val: str = cnf.YN_REPL_VAL,
                       bin_src_col: str = cnf.BIN_SRC_COL_AGE,
                       bin_tgt_col: str = cnf.BIN_TGT_COL_AGE,
                       bin_cuts: List[int] = cnf.CUT_BINS_AGE,
                       bin_labels: List[str] = cnf.BINS_LABELS_AGE
                       ) -> None:
    """
    generating preprocessed dataframe from vaers data

    Params:
    -------
    path : (str) file path where to look for files
    pattern : (str) regex pattern for matching files
    dt_cols : (list of str) list of columns to be converted
    dt_format : (str) strf representation of date format in cols
    nan_cols : (list of str) columns to be converted
    nan_repl_val : (str) value to replace nans
    bin_src_col : (str) column to be binned
    bin_tgt_col : (str) column to store binning results
    bin_cuts : (list of int) list values at which to cut_bins
    bin_labels : (list of str) labels to be used for bins


    Returns:
    --------
    df : (dataframe) preprocessed dataframe
    """
    pass
    # loading data
    fps = setup_filepaths(path, pattern)
    df = compile_df(fps)

    # data preprocessing
    df = convert_to_datetime(df, dt_cols, dt_format)
    df = convert_nans(df, nan_cols, nan_repl_val)
    df = create_binning(df, bin_src_col, bin_tgt_col,
                        bin_cuts, bin_labels)
    return df
