from yahoo_finance import Share
import googlefinance


class StockData:

    def __init__(self):
        self.stockdata = {
            "AETI": {
                "symbol": "AETI",
                "name": "American Electric Technologies Inc",
                "exchange": "NASDAQ"
            },
            "CRNT": {
                "symbol": "CRNT",
                "name": "Ceragon Networks Ltd",
                "exchange": "NASDAQ"
            }
        }

    def get_stock_info(self, symbol):
        # stock = googlefinance.getQuotes(symbol)
        # stockinfo = googlefinance.request([symbol])
        # url = googlefinance.buildUrl([symbol])
        # print(stockinfo)
        # print(type(stockinfo))
        # print(dir(stockinfo))
        # print(url)
        stock = Share(symbol)
        # print(type(stock))
        # print(stock.get_info())
        print(stock.data_set)

        # print(stock.get_earnings_share())
        print("**********************")
        # return self.stockdata.get(symbol)
        return stock
