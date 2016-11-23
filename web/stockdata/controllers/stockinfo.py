from stockdata.services.yahoo_finance_client import YahooFinanceClient
import pandas as pd


class StockData:

    def get_stock_info(self, symbol):
        stockinfo = YahooFinanceClient().get_stock_info(symbol)
        if stockinfo is None:
            return None

        return {
            "symbol": symbol,
            "name": stockinfo['name'],
            "exchange": stockinfo['exchange'],
            "current_price": stockinfo['current_price'],
            "year_high": stockinfo['year_high'],
            "pv_trend_data": self.get_pv_trend_data(stockinfo['price_history'])
        }

    def get_pv_trend_data(self, price_history):
        df = pd.DataFrame(price_history)
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
            "pv_data": df[['Volume', 'Date', 'pct_change']].to_dict('records')
        }
        return pv_trend_data
