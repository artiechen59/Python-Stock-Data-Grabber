from finlab.crawler import table_date_range, update_table, to_pickle, out, commit,merge
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
#import pandas_datareader.data as web
from datetime import datetime, timedelta,date
import os
from openpyxl import load_workbook

#===========================
https://query1.finance.yahoo.com/v7/finance/download/%5ETWII?period1=852076800&period2=1594512000&interval=1d&events=history
#   https://finance.yahoo.com/quote/%5ETWII/history?p=%5ETWII         , select start and end date, then download the csv file
#==================================

df = pd.read_pickle("history/tables/TWII_complete.pkl")
print(df)

exit()
reader_price=pd.read_csv('^TWII.csv',index_col='Date')

#print(reader_price.head())
#print('======================')
reader_price.index=pd.to_datetime(reader_price.index)
#print(reader_price.head())


reader_price.index.name = 'date'
reader_price = reader_price.reset_index()
reader_price['stock_id'] = '台股指數'
reader_price = reader_price.set_index(['stock_id', 'date'])


print(reader_price)
reader_price.to_pickle("./history/tables/TWII_complete.pkl")
