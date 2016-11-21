from stockdata.services.yahoo_finance_client import YahooFinanceClient


class StockData:

    def get_stock_info(self, symbol):
        stockinfo = YahooFinanceClient().get_stock_info(symbol)
        if stockinfo is None:
            return None

        # df_historical_data = pd.DataFrame(historical_data)
        # for key in ['Volume', 'Open', 'Close']:
        #     df_historical_data[key] = pd.to_numeric(df_historical_data[key])


        # df_historical_data['pct_change'] = (df_historical_data['Close'] - df_historical_data['Open']) / df_historical_data['Open'] * 100
        # df_historical_data['pct_change'] = df_historical_data['pct_change'].round(1)
        # print(df_historical_data)
        # print(df_historical_data.describe().round(2))

        return {
            "symbol": symbol,
            "name": stockinfo['name'],
            "exchange": stockinfo['exchange'],
            "current_price": stockinfo['current_price'],
            "year_high": stockinfo['year_high'],
        }
