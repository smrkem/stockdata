from flask import render_template, request, json
from stockdata import app
from stockdata.controllers.stockinfo import StockData

@app.route('/', methods=['GET', 'POST'])
def index():
    stockinfo = None
    errors = []
    if request.method == 'POST' and request.form['symbol']:
        stock = StockData(request.form['symbol'])
        stockinfo = stock.get_stock_info()
        if stockinfo is None:
            errors.append("Could not find any stock for symbol: '{}'".format(request.form['symbol']))
        else:
            stockinfo['pv_history_data'] = json.dumps(stock.get_pv_trend_data())
    return render_template('index.html', stock=stockinfo, errors=errors)
