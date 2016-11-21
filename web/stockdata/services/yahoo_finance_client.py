from yahoo_finance import Share
import datetime


class YahooFinanceClient:

    def get_stock_info(self, symbol):
        stock = Share(symbol)
        stock_name = stock.get_name()
        if stock_name is None:
            return None
        stock_exchange = stock.get_stock_exchange()
        current_price = stock.get_price()
        year_high = stock.get_year_high()

        today = datetime.date.today()
        last_year = today - datetime.timedelta(days=368)
        historical_data = stock.get_historical(str(last_year), str(today))

        return {
            "name": stock_name,
            "exchange": stock_exchange,
            "current_price": current_price,
            "year_high": year_high,
            "price_history": historical_data
        }
