from yahoo_finance import Share
import datetime
import pandas as pd


class YahooFinanceClient:

    def get_stock_info(self, symbol):
        stock = Share(symbol)
        stock_name = stock.get_name()
        if stock_name is None:
            return None
        stock_exchange = stock.get_stock_exchange()
        current_price = stock.get_price()
        year_high = stock.get_year_high()

        # today = datetime.date.today()
        # last_year = today - datetime.timedelta(days=313)
        # historical_data = stock.get_historical(str(last_year), str(today))
        # historical_df = pd.DataFrame(historical_data)
        # print(historical_df)

        return {
            "symbol": symbol,
            "name": stock_name,
            "exchange": stock_exchange,
            "current_price": current_price,
            "year_high": year_high
        }
