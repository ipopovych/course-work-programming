import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import plotly

plotly.plotly.sign_in('ipopovych', 'X6V8yMuv7zWFidNmqFVT')


def check_date(year, date, days=False):
    """
    :param date: date in string format, e.g. '2006-12-25 00:00:00+02'
    :param days: if True, days are left in the date string, not otherwise
    :return None if date is not valid, date string 'yyyy-mm' otherwise
    """
    k = 10 if days else 7
    # cleaning files and decisions tht were adjustificated not in current processing year
    if str(year) not in str(date):
        return None
    else:
        return str(date)[:k]


def clear_df(dataframe, year, days=False, **kwargs):
    """
    :param dataframe: pandas dataframe
    :param year: integer, year dataframe contains information of
    :param days: if True, dates are left including the days
    :param kwargs: adjudication_date, justice_kind, judgment_code, category_code could be specified
    :return: new filtered dataframe
    """
    PARAMETERS = ['adjudication_date', 'justice_kind', 'judgment_code', 'category_code']
    fltr = [str(key) for key in kwargs.keys() if (kwargs[key] and str(key) in PARAMETERS)]

    df = dataframe.filter(fltr, axis=1)
    #print(df)

    # Removing days from dates
    df['adjudication_date'] = df['adjudication_date'].apply(lambda x: check_date(year, x, days))
    #print('checked date', df)

    # Removing empty and invalid date values
    df = df[df.adjudication_date.notnull()]

    # Counting number of occurrences of the same dates, adding count column
    df['freq_date'] = df.groupby('adjudication_date')['adjudication_date'].transform('count')

    # deleting same dates
    df = df.drop_duplicates('adjudication_date')

    # Converting dates to datetime
    if days:
        df['adjudication_date'] = df['adjudication_date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
    else:
        df['adjudication_date'] = df['adjudication_date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m'))

    return df


def plot(dataframe, title, online=True):
    """
    Plots the dataframe as a plotly plot online.
    :param dataframe: pandas dataframe
    :param title: title to put in the plot
    :param online: if True, plots online
    :return: None
    """
    data = [go.Scatter(x=dataframe['adjudication_date'],
                       y=dataframe['freq_date'],
                       mode='markers',
                       marker=dict(size='16',
                                   color=dataframe['freq_date'],  # set color equal to a variable
                                   colorscale='Viridis',
                                   showscale=True
                                   ))]

    layout = dict(title=title)
    if online:
        plotly.plotly.plot(dict(data=data, layout=layout), filename='{}.html'.format(title))
    else:
        plotly.offline.plot(dict(data=data, layout=layout), filename='{}.html'.format(title))


def plot_year(year, files, days=True, online=False):
    df = pd.read_csv(files[year], delimiter="\t")
    df = clear_df(df, year, days=days, adjudication_date=True, category_code=True)
    if days:
        plot(df, online=online, title='Кількість судових рішень прийнятих за {} рік, щоденно'.format(year))
    else:
        plot(df, online=online, title='Кількість судових рішень прийнятих за {} рік, за місяцями'.format(year))


def plot_years(years, files, days=True, online=False):
    data = []
    for y in years:
        filename = files[y]
        df = pd.read_csv(filename, delimiter="\t")
        df = clear_df(df, y, days=days, adjudication_date=True, category_code=True)
        data.append(df)

    data = pd.concat(data)
    if days:
        plot(data, online=online, title='Кількість судових рішень прийнятих за {}-{} роки, щоденно'.format(years[0], years[-1]))
    else:
        plot(data, online=online, title='Кількість судових рішень прийнятих за {}-{} роки, за місяцями'.format(years[0], years[-1]))
