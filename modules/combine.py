import plotly.plotly as py
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import plotly

py.sign_in('ipopovych', 'X6V8yMuv7zWFidNmqFVT')
years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]


def check_date(date):
    global year
    if str(year) not in str(date):
        return None
    else:
        return str(date)[:10]

# filename = "data/{}/documents.csv".format(year)
# df = pd.read_csv(filename, delimiter="\t")
# df = df[~df["adjudication_date"].isnull()]
#
#
# # Removing days from dates
# df['adjudication_date'] = df['adjudication_date'].apply(lambda x: check_date(x))
#
# # Removing invalid dates
# df = df[~df.astype(str).eq('None').any(1)]
#
# # Counting number of occurrences of the same dates year-month
# df['freq_date'] = df.groupby('adjudication_date')['adjudication_date'].transform('count')
#
# # Converting dates to datetime
# df['adjudication_date'] = df['adjudication_date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
#
# # deleting same dates
# df = df.drop_duplicates('adjudication_date')
#
# fdf = df[['adjudication_date', 'freq_date']].copy()

dat = []

for year in years:
    filename = "data/{}/documents.csv".format(year)
    df = pd.read_csv(filename, delimiter="\t")
    df = df[~df["adjudication_date"].isnull()]
    df['adjudication_date'] = df['adjudication_date'].apply(lambda x: check_date(x))
    df = df[df.adjudication_date.notnull()]
    df['freq_date'] = df.groupby('adjudication_date')['adjudication_date'].transform('count')
    df['adjudication_date'] = df['adjudication_date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
    df = df.drop_duplicates('adjudication_date')
    fdf = df[['adjudication_date', 'freq_date']].copy()
    dat.append(fdf)

dat = pd.concat(dat)

data = [go.Scatter(x=dat['adjudication_date'],
                   y=dat['freq_date'],
                   mode='markers',
                   marker=dict(size='16',
                               color=dat['freq_date'],  # set color equal to a variable
                               colorscale='Viridis',
                               showscale=True
        ))]

layout = dict(title='Кількість судових рішень прийнятих в Україні за 2006-2018 роки, за днями')


plotly.offline.plot(dict(data=data, layout=layout), filename='days-2006-2018.html')