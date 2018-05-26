import plotly.plotly as py
import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import plotly


py.sign_in('username', 'api-key')
years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]


def check_date(date, coef=10):
    """
    :param coef: integer, 7 or 10. If 10, days are left in data fields, otherwise not.
    :param date: date in string format 'yyyy-mm-dd hh-mm-ss+hh', e.g. '2006-12-25 00:00:00+02'
    :return:
    """
    global year
    if str(year) not in str(date):
        return None
    else:
        return str(date)[:coef]


dat = []

for year in years:
    filename = "data/{}/documents.csv".format(year)
    df = pd.read_csv(filename, delimiter="\t")
    df['adjudication_date'] = df['adjudication_date'].apply(lambda x: check_date(x))  # checking every date
    df = df[df.adjudication_date.notnull()]
    df['freq_date'] = df.groupby('adjudication_date')['adjudication_date'].transform('count')  # Counting number of occurrences of the same dates
    df['adjudication_date'] = df['adjudication_date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
    df = df.drop_duplicates('adjudication_date')  # deleting similar dates
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