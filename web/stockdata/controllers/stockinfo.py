from stockdata.services.yahoo_finance_client import YahooFinanceClient


class StockData:

    def get_stock_info(self, symbol):
        return YahooFinanceClient().get_stock_info(symbol)
