from yahoo_finance import Share


class YahooFinanceClient:

    def get_stock_info(self, symbol):
        stock = Share(symbol)
        return {
            "symbol": symbol,
            "name": stock.get_name(),
            "exchange": stock.get_stock_exchange()
        }
