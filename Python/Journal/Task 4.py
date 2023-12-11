import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
from matplotlib.dates import DateFormatter
import numpy as np

con = sqlite3.connect('DATA.sqlite')
df = pd.read_sql_query("SELECT * from Data", con)

# current date
today = date.today()
date = today.strftime('%Y-%m-%d')


date = df['Date'].iloc[-1]
# check if the last date is a sunday. monday = 0, sunday =6
isSunday = datetime.fromisoformat(df['Date'].iloc[-1]).weekday() == 6

# isSunday = True

if isSunday:
    df['Date_new'] = pd.to_datetime(df['Date']) - pd.to_timedelta(7, unit='d')
    weekly_df = df.resample('W-Sun', on='Date_new').sum().reset_index()
    df3 = ((df.groupby(df.Date_new).Alcohol.value_counts(normalize=True)).unstack().fillna(0)).reset_index().resample(
        'W-Sun', on='Date_new').sum()
    df4 = df3.reset_index()
    df4['Date_new'] = df4['Date_new'].astype(str)
    weekly_df.Date_new = weekly_df.Date_new.astype(str)

    # plot weekly sleep
    fig = plt.figure(figsize=(20, 10))

    X = weekly_df.Date_new.tolist()

    X_axis = np.arange(len(X))
    # plot the graph
    plt.bar(X_axis, weekly_df.Sleeping_hours)

    plt.xticks(X_axis, X)
    plt.title('Total sleep per Week')
    plt.xlabel('Week')
    plt.ylabel('Hours')

    plt.savefig('./' + str(today) + '_weekly_sleep.jpg', bbox_inches='tight')

    fig = plt.figure(figsize=(20, 10))
    X = weekly_df.Date_new.tolist()
    X_axis = np.arange(len(X))
    plt.bar(X_axis, weekly_df.Cigarettes)
    plt.xticks(X_axis, X)
    plt.title('Cigarettes per Week')
    plt.xlabel('Week')
    plt.ylabel('Cigarettes')
    plt.savefig('./' + str(today) + '_weekly_cigarettes.jpg', bbox_inches='tight')

    # this is a categorical variable. We have to plot seperately Yes and No instances.
    X = df4.Date_new.tolist()
    X_axis = np.arange(len(df4.Date_new))
    fig = plt.figure(figsize=(20, 10))

    # plot yes and no seperately.
    plt.bar(X_axis - 0.2, df4.Yes, 0.4, label='Yes')
    plt.bar(X_axis + 0.2, df4.No, 0.4, label='No')
    plt.xticks(X_axis, X)
    plt.xlabel('Week')
    plt.ylabel('Days')
    plt.title('Days of with and without alcohol per week')

    plt.legend()
    plt.savefig('./' + str(today) + '_weekly_alcohol.jpg', bbox_inches='tight')

else:
    # plot cigarettes
    fig = plt.figure(figsize=(20, 10))
    plt.bar(df.Date, df.Cigarettes)
    plt.xlabel('Date')
    plt.ylabel('Number of Cigarettes')
    plt.title('Cigarrettes per Day')
    plt.savefig('./' + str(today) + '_cigarettes.jpg', bbox_inches='tight')

    # plot sleeptime
    fig = plt.figure(figsize=(20, 10))
    plt.bar(df.Date, df.Sleeping_hours)
    plt.xlabel('Date')
    plt.ylabel('Sleeping Hours')
    plt.title('Sleeping Hours per Day')
    plt.savefig('./' + str(today) + '_sleeping_hours.jpg', bbox_inches='tight')

    # plot Alcohol
    fig = plt.figure(figsize=(20, 10))
    plt.plot(df.Date, df.Alcohol)
    plt.xlabel('Date')
    plt.ylabel('Alcohol')
    plt.title('Date vs Alcohol')
    plt.savefig('./' + str(today) + '_Alcohol.jpg', bbox_inches='tight')
