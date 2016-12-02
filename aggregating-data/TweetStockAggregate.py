# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

from datetime import datetime


tweets = pd.read_csv("Tweets.csv")
stocks = pd.read_csv("StockPrices.csv")

#add new datetime and day column to dataframe
tweets_created_dt = pd.to_datetime(tweets.loc[:, 'tweet_created'])
tweets['tweets_created_dt'] = tweets_created_dt
tweets['created_dt'] =  tweets['tweets_created_dt'].dt.day

#new day column to stocks df
stocks['day'] = pd.to_datetime(stocks.loc[:, 'Date']).dt.day


#map the stocks according to airline and date

stocks.loc[(stocks['airline'] == 'Virgin America') & (stockss['created_dt'] == 17)]

tweets.loc[(tweets['airline'] == 'Virgin America') & (tweets['created_dt'] == 17)]
