from finlab.crawler import table_date_range, update_table, to_pickle, out, commit, merge, date_range
import requests
from bs4 import BeautifulSoup
import time

import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
# import pandas_datareader.data as web
from datetime import datetime, timedelta, date
import os
from openpyxl import load_workbook
import datetime


def get_shareholder(company_id):
    stock_id = company_id[:company_id.find(' ')]

    #print(stock_id)

    # https://goodinfo.tw/StockInfo/EquityDistributionClassHis.asp?STOCK_ID=00722B&CHT_CAT=WEEK&STEP=DATA&DISPLAY_CAT=SHAREHOLD_RATIO
    URL = 'https://goodinfo.tw/StockInfo/EquityDistributionClassHis.asp?STOCK_ID=' + stock_id + '&CHT_CAT=WEEK&STEP=DATA&DISPLAY_CAT=SHAREHOLD_RATIO'
    my_headers = {'referer': 'https://goodinfo.tw/StockInfo/EquityDistributionClassHis.asp?STOCK_ID=' + stock_id,
                  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    #print(URL)

    try:
        response = requests.post(URL, headers=my_headers)
        # response = requests.get(URL)
        time.sleep(1)
    except:
        time.sleep(30)
        # response = requests.get(URL)
        response = requests.post(URL, headers=my_headers)
        time.sleep(1)

    # print(response.status_code)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    dataStart = False
    data = []
    data.append([])
    data_index = 0
    trs = soup.find_all('tr')

    #print(len(trs))
    if len(trs) != 0:

        for i in range(4, len(trs)):

            tds = trs[i].find_all('td')
            if len(tds[1].get_text()) == 0:
                continue
            a = tds[0].get_text()
            if a.find('週別') == -1 and a.find('收盤') == -1:
                year = "20" + tds[0].get_text()[:tds[0].get_text().find("W")]
                month = tds[1].get_text()[:tds[1].get_text().find("/")]
                day = tds[1].get_text()[tds[1].get_text().find("W") - 1:]

                data[data_index].append(company_id)  # stock id

                data[data_index].append(datetime.datetime(int(year), int(month), int(day)))  # date
                data[data_index].append(tds[2].get_text())  # 收盤
                data[data_index].append(tds[3].get_text())  # 漲跌元
                data[data_index].append(tds[4].get_text())  # 漲跌幅

                data[data_index].append(tds[5].get_text())  #
                data[data_index].append(tds[6].get_text())  #
                data[data_index].append(tds[7].get_text())  #
                data[data_index].append(tds[8].get_text())  #
                data[data_index].append(tds[9].get_text())  #
                data[data_index].append(tds[10].get_text())  #
                data[data_index].append(tds[11].get_text())  #
                data[data_index].append(tds[12].get_text())  #

                # data[data_index].append(datetime.datetime(year,month,10))  #date
                # data[data_index].append(str(int(float(tds[7].get_text().replace(',',''))*100000)))   #當月營收
                # data[data_index].append(tds[8].get_text().replace('+',''))                          #上月比較增減(%)
                # data[data_index].append(tds[9].get_text().replace('+',''))                          #去年同月增減(%)
                # data[data_index].append(str(int(float(tds[10].get_text().replace(',',''))*100000)))  #當月累計營收
                # data[data_index].append(tds[11].get_text().replace('+',''))                          #前期比較增減(%)

                data.append([])
                data_index = data_index + 1

        df1 = pd.DataFrame(data,
                           columns=['stock_id', 'date', '收盤', '漲跌(元)', '漲跌(%)', '10張以下(%)', '10至50張(%)', '50至100張(%)',
                                    '100至200張(%)', '200至400張(%)', '400至800張(%)', '800至1千張(%)', '超過1千張(%)'])

        # df['stock_id']=company_id
        df1 = df1.set_index(['stock_id', 'date'])
        df1 = df1.dropna(how='all', axis=0)  # .dropna(how='all', axis=1)
        df1 = df1.sort_index(level='date', ascending=True)

    return df1

#df = pd.read_pickle("history/tables/monthly_report_new.pkl")
df = pd.read_pickle("history/tables/share_hold.pkl")
#print(df[df.index.get_level_values('stock_id')=="1101 台泥"])
print(df.shape)
#print(df.index.get_level_values('stock_id').drop_duplicates())
print(len(df.index.get_level_values('stock_id').drop_duplicates()))


reader_list = pd.read_excel('stocklist.xlsx',sheet_name='list')
stocklist = reader_list.iloc[ : , 0 ]
stockname= reader_list.iloc[ : , 1 ]

df_combined=pd.DataFrame()

for k in range(30,40):
    df_tmp=get_shareholder(stocklist[k]+' '+stockname[k])
    time.sleep(10)
    df_combined=df_combined.append(df_tmp)
    print(str(k)+'..Done...'+stocklist[k]+' '+stockname[k])
print(df_combined.shape)

df=df.append(df_combined)
df=df.sort_index()
to_pickle(df, 'share_hold')

commit()