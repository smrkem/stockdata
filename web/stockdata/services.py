from yahoo_finance import Share
import pandas as pd
import numpy as np
from pyquery import  PyQuery as pq
import requests

class StockData:

    def __init__(self):
        self.column_headers = None
        self.column_data = None
        self.symbol = None
        self.exchange = None

    def get_stock_info(self, symbol):
        self.exchange = "NASDAQ"
        self.symbol = symbol
        self.fetch_stock_info(self.symbol, self.exchange)

        if not self.column_data:
            return None
        return {
            'symbol': self.symbol,
            'exchange': self.exchange,
            'financials': {
                'headers': self.column_headers,
                'data': self.column_data
            }
        }

    def fetch_stock_info(self, symbol, market):
        page = requests.get("https://www.google.com/finance?q={}:{}&fstype=ii".format(self.exchange, self.symbol))
        table = pq(page.content.decode('utf8'))
        table1 = table("#app #incinterimdiv table#fs-table")
        if table1.html() is None:
            print("Yes. table1 is None")
            print("************")
        else:
            dataframe_list = pd.read_html("<table>{}</table>".format(table1.html()))
            df = dataframe_list[0]
            df.set_index('In Millions of USD (except for per share items)', inplace=True)
            df.replace('-', np.nan, inplace=True)
            df.dropna(how='all', inplace=True)
            self.column_headers = list(df.columns.values)
            self.column_data = df.T.to_dict('list')

