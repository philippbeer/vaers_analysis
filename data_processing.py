
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

if __name__ == "__main__":
    fps = setup_filepaths(cnf.PATH,
                          cnf.FILENAME_PATTERN)

    df = compile_df(fps)
    print(df.head())
