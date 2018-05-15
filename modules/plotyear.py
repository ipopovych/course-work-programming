import pandas as pd
from datetime import datetime
import plotly.graph_objs as go
import plotly


def check_date(date):
    """
    :param date: date in string format, e.g. '2006-12-25 00:00:00+02'
    :return None if date is not valid, date string 'yyyy-mm' otherwise
    """
    global year
    if str(year) not in str(date):
        return None
    else:
        return str(date)[:7]


year = 2015  # year to plot decisions
print('processing year {}'.format(year))

filename = "data/{}/documents.csv".format(year)
df = pd.read_csv(filename, delimiter="\t")


# Removing days from dates
df['adjudication_date'] = df['adjudication_date'].apply(lambda x: check_date(x))

# Removing empty and invalid date values
df = df[df.adjudication_date.notnull()]

# Counting number of occurrences of the same dates year-month
df['freq_date'] = df.groupby('adjudication_date')['adjudication_date'].transform('count')

# Converting dates to datetime
df['adjudication_date'] = df['adjudication_date'].apply(lambda x: datetime.strptime(str(x), '%Y-%m'))

# deleting same dates
df = df.drop_duplicates('adjudication_date')

data = [go.Scatter(x=df['adjudication_date'],
                       y=df['freq_date'],
                       mode='markers',
                       marker=dict(size='16',
                                   color=df['freq_date'],  # set color equal to a variable
                                   colorscale='Viridis',
                                   showscale=True
            ))]

layout = dict(title='Кількість судових рішень за {} рік'.format(year))


plotly.offline.plot(dict(data=data, layout=layout), filename='{}.html'.format(year))
