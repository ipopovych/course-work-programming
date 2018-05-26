from cleaner import get_filenames, Cleaner
from plotter import plot_year, plot_years
import pandas as pd
from input import get_year, specify
import os

CATEGORY_FILTERS = {'military': 'filters/military.csv'}
DATAFILES_PATH = os.curdir

yearfiles = get_filenames(DATAFILES_PATH)  # dictionary with paths to data files
YEARS = sorted([k for k in yearfiles.keys()])  # list of years that are included in the data
filters = pd.Series.from_csv(CATEGORY_FILTERS['military'], header=None).to_dict()  # category code filters (codes to include)

YEARS = list(get_year())

if YEARS:
    topic = specify(CATEGORY_FILTERS)

if len(YEARS) == 1:
    plot_year(YEARS[0], yearfiles)
else:
    plot_years(YEARS, yearfiles)






