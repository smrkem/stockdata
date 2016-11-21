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
