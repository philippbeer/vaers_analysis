PATH = "all_data/"

FILENAME_PATTERN = ".*VAERSDATA.csv"

DATE_FORMAT = "%m/%d/%Y"

DATE_COLS = ['RECVDATE',
             'DATEDIED',
             'VAX_DATE',
             'ONSET_DATE',
             'TODAYS_DATE']

YN_COLS = ['DIED',
           'HOSPITAL']

YN_REPL_VAL = "N"

# BINNING Paramaters
CUT_BINS_AGE = [0, 15, 25, 35, 45, 55, 65, 75, 85, 120]
BINS_LABELS_AGE = ["0-15", "15-25", "25-35", "35-45", "45-55", "55-65", 
         "65-75", "75-85", ">85"]
