#!/usr/bin/env /Users/vkamlesh/.virtualenvs/finpy/bin/python
import bs4 as bs
import datetime as dt
import os
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt 
from matplotlib import style
import matplotlib.dates as mdates
import seaborn as sns
import pickle 
import requests
from collections import Counter
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
#print(style.available)
style.use('ggplot')
def save_nifty50_tickers():
    resp = requests.get("https://en.wikipedia.org/wiki/NIFTY_50").text
    soup = bs.BeautifulSoup(resp, 'lxml')
    table = soup.find('table',{'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        tickers.append(ticker)
    
    with open("nifty50.pickle", "wb") as f:
        pickle.dump(tickers, f)
    print(tickers)
    return tickers

def get_data_from_yahoo(reload_nifty50=False):
    if reload_nifty50:
        tickers = save_nifty50_tickers()
    else:
        with open("nifty50.pickle","rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dir'):
        os.makedirs('stock_dir')

    start = dt.datetime(2000,1,1)
    end = dt.datetime(2020,12,29)

    for ticker in tickers:
        print(tickers)
        if not os.path.exists('stock_dir/{}.csv'.format(tickers)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.to_csv('stock_dir/{}.csv'.format(ticker))
        else:
           print('Already have {}'.format(ticker))
 


def compile_nifty50():
    with open("nifty50.pickle","rb") as f:
        tickers = pickle.load(f)
    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv('stock_dir/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        
        df.rename(columns = {'Adj Close':ticker}, inplace=True)
        df.drop(['High','Low','Open','Close','Volume'], 1, inplace=True)
        if main_df.empty:
            main_df = df
        else:
             main_df = main_df.join(df, how='outer') #outer: form union of calling frame’s index (or column if on is specified) with other’s index, and sort it. lexicographically.
        
        if count % 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('nifty50_joined_close.csv')     


def visualize_date():
    df = pd.read_csv('nifty50_joined_close.csv')
    df_corr = df.corr()
    sns.heatmap(df_corr,cmap='RdYlGn', vmin=-1, vmax=1)
    plt.show()


def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('nifty50_joined_close.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)

    for i in range(1, hm_days+1):
        df['{}_{}d'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]

    df.fillna(0, inplace=True)
    return tickers, df
    

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02 #if stock fall or gain 2%
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0


def extract_featuressets(ticker):
    tickers, df = process_data_for_labels(tickers)

    df['{}_target'.format(ticker)] = list(map(buy_sell_hold, * [df['{}_{}d'.format(ticker,i)] for i in range(1, hm_days+1)]))
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [sttr(i) for i in vals]
    print('Data spread:', Counter(str_vals))

    df.fallna(0, implace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[ticke for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    x = df_vals.values
    y = df['{}_target'.format(ticker)].values

    return X, y, df






    










    








