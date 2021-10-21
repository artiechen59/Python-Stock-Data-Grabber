from finlab.crawler import table_date_range, update_table, to_pickle, out, commit,merge, date_range
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

import os
from openpyxl import load_workbook

df = pd.read_pickle("history/tables/price_2021.pkl")
print(len(df.index.get_level_values('stock_id').drop_duplicates()))
#print(df.index.get_level_values('stock_id').drop_duplicates())
#print(df.tail())