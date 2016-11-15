class StockData:

    def __init__(self):
        self.sources = list()
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
        stockdata = self.sources[0].get_stock_info(symbol)
        return self.stockdata.get(symbol)
