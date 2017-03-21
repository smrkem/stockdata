from stockdata.services.yahoo_finance_client import YahooFinanceClient
import pandas as pd
import pickle, os


class StockData:

    def __init__(self, symbol):
        if (self.get_from_cache(symbol)):
            return

        self.stockinfo = YahooFinanceClient().get_stock_info(symbol)
        if self.stockinfo is not None:
            self.stockinfo['symbol'] = symbol
            self.save_to_cache()

    def get_stock_info(self):
        if self.stockinfo is None:
            return None

        return {
            "symbol": self.stockinfo['symbol'],
            "name": self.stockinfo['name'],
            "exchange": self.stockinfo['exchange'],
            "current_price": self.stockinfo['current_price'],
            "year_high": self.stockinfo['year_high']
        }

    def get_pv_trend_data(self):
        df = pd.DataFrame(self.stockinfo['price_history'])
        for key in ['Volume', 'Open', 'Close']:
            df[key] = pd.to_numeric(df[key])
        df['pct_change'] = round(
            (df['Close'] - df['Open']) / df['Open'] * 100,
            1
        )

        df_stats = df.describe()
        pv_trend_data = {
            "max_volume": df_stats['Volume']['max'],
            "min_volume": df_stats['Volume']['min'],
            "volume_p75": df_stats['Volume']['75%'],
            "pv_data": df[['Volume', 'Date', 'pct_change']].to_dict('records')
        }
        return pv_trend_data

    def save_to_cache(self):
        if not os.getenv('CACHING'):
            return False

        filepath = 'tests/data/TEST_{}_PICKLE.pk1'.format(self.stockinfo['symbol'])
        with open(filepath, 'wb') as output:
            pickle.dump(self.stockinfo, output, pickle.HIGHEST_PROTOCOL)

    def get_from_cache(self, symbol):
        if not os.getenv('CACHING'):
            return False

        filepath = 'tests/data/TEST_{}_PICKLE.pk1'.format(symbol)
        if (os.path.isfile(filepath)):
            with open(filepath, 'rb') as input:
                self.stockinfo = pickle.load(input)
            return True
        else:
            return False
