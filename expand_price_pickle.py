from finlab.crawler import table_date_range, update_table, to_pickle, out, commit,merge
import datetime
from io import StringIO
import requests
from bs4 import BeautifulSoup
import time

import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
#import pandas_datareader.data as web
from datetime import datetime, timedelta,date
import os
from openpyxl import load_workbook




df = pd.read_pickle("history/tables/price_new.pkl")
#print(df.shape) org (11383416,9) up to 2019/7/19


reader_list = pd.read_excel('allstocklist1.xlsx', sheet_name='price', names=None)
stocklist = reader_list.iloc[:, 0]
stockCount = 0
total_Data=0
combined_df=pd.DataFrame()

# print(stocklist)
for stock in stocklist:
    stockCount = stockCount + 1
    print('Updating stock ' + stock + '...' + str(stockCount) + '/' + str(len(stocklist)))
    # print(df[df.index.get_level_values('stock_id')==stock].sort_index(level='date', ascending=True).head(1).index.get_level_values('date'))   #get the 1st date
    endDate = df[df.index.get_level_values('stock_id') == stock].sort_index(level='date', ascending=True).head(1).index.get_level_values('date')


    endDate = endDate - timedelta(days=1)


    URL = 'http://www.cnyes.com/twstock/ps_historyprice/' + stock[:stock.find(' ')] + '.htm'
    form_data = {
        'pageTypeHidden': '1', 'code': stock[:stock.find(' ')], 'ctl00$ContentPlaceHolder1$startText': '1950/01/01',
        'ctl00$ContentPlaceHolder1$endText': endDate[0].strftime("%Y/%m/%d"), 'ctl00$ContentPlaceHolder1$submitBut': '查詢'
    }


    try:
        response = requests.post(URL, data=form_data)
        time.sleep(1)
    except:
        time.sleep(30)
        response = requests.post(URL, data=form_data)
        time.sleep(1)



    # print(response.status_code)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    trs = soup.find_all('tr')

    if len(trs) < 5:
        print('2nd try ....')
        time.sleep(5)
        response = requests.post(URL, data=form_data)
        time.sleep(1)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        trs = soup.find_all('tr')
    if len(trs) < 5:
        print('3rd try ....')
        time.sleep(5)
        response = requests.post(URL, data=form_data)
        time.sleep(1)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        trs = soup.find_all('tr')

    # print(trs)
    dayCode = []
    opening = []
    high = []
    low = []
    close = []
    volumestock = []
    volumemoney = []

    # print(trs[1])
    # print(trs[0])   #日期 開盤 最高 最低 收盤 漲跌 漲% 成交量 成交金額 本益比

    # print(trs[len(trs)-3]) # oldest data: trs[len(trs)-3], newest data trs[1]
    for j in range(len(trs) - 3, 0, -1):
        tds = trs[j].find_all('td')

        format_str = '%Y/%m/%d'  # The format
        datetime_obj = datetime.strptime(tds[0].get_text(), format_str)
        dayCode.append(datetime_obj.date())
        opening.append(float(tds[1].get_text().replace(',', '')))
        high.append(float(tds[2].get_text().replace(',', '')))
        low.append(float(tds[3].get_text().replace(',', '')))
        close.append(float(tds[4].get_text().replace(',', '')))
        volumestock.append(int(float(tds[7].get_text().replace(',', '')) * 1000))
        volumemoney.append(int(float(tds[8].get_text().replace(',', '')) * 1000))

    # writer = ExcelWriter(filename, engine='openpyxl')
    # df = pd.DataFrame(columns=header)
    df1 = pd.DataFrame({
        'stock_id': stock,
        'date': dayCode,
        '成交股數': volumestock,
        '成交金額': volumemoney,
        '收盤價': close,
        '開盤價': opening,
        '最低價': low,
        '最高價': high,
    })
    # df = pd.DataFrame(dayCode)

    df1 = df1.set_index(['stock_id', 'date'])
    print(df1.shape)
    combined_df = combined_df.append(df1)
    #print(endDate)
    #print(combined_df)
    total_Data=total_Data+df1.shape[0]
    print(total_Data)

    #exit()

    #print(df1.shape,combined_df.shape)
    #print('==================================================')
    time.sleep(5)
    if (stockCount>0) :#and (stockCount%10 ==1):
        if total_Data > 0:
            print('Now saving data....')
            to_pickle(combined_df, 'price_new')
            print('Done saving data....')
            combined_df = pd.DataFrame()
            total_Data=0
            #exit()
    # if stock=='0053 元大電子':
    #     print(combined_df.head())
    #     print(combined_df.tail())
    #
    #     print(combined_df[combined_df.index.get_level_values('stock_id') == '0015 富邦'].shape)
    #     print(combined_df[combined_df.index.get_level_values('stock_id') == '0050 元大台灣50'].shape)
    #     print(combined_df[combined_df.index.get_level_values('stock_id') == '0051 元大中型100'].shape)
    #     print(combined_df[combined_df.index.get_level_values('stock_id') == '0052 富邦科技'].shape)
    #     break
#df = pd.read_pickle("history/tables/price_new.pkl")

#to_pickle(df1, 'test')
#print(df.head())
#print(df[df.index.get_level_values('stock_id')=='0015 富邦'].head())
#print(df[df.index.get_level_values('stock_id')=='0015 富邦'].tail())


#commit()
#======================================================================================
#allID = df.index.get_level_values('stock_id')
#allID = list(dict.fromkeys(allID))  # remove duplicates
#print(df1.index.get_level_values('date'))


#from openpyxl import load_workbook
#from pandas import ExcelWriter
#writer = ExcelWriter('allstocklist.xlsx', engine='openpyxl')
#df1 = pd.DataFrame(allID)
#df1.to_excel(writer, sheet_name='price', header=False, index=False)
#writer.save()