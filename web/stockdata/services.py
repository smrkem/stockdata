from stockdata.sources.YahooFinanceClient import YahooFinanceClient


class StockData:

    def get_stock_info(self, symbol):
        return YahooFinanceClient().get_stock_info(symbol)
