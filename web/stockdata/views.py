from flask import render_template, request, json
from stockdata import app
from stockdata.controllers.stockinfo import StockData

@app.route('/', methods=['GET', 'POST'])
def index():
    stock = None
    errors = []
    if request.method == 'POST' and request.form['symbol']:
        stock = StockData().get_stock_info(request.form['symbol'])
        if stock is None:
            errors.append("Could not find any stock for symbol: '{}'".format(request.form['symbol']))
        # else:
        #     stock['pv_trend_data'] = json.dumps(stock['pv_trend_data'])
    return render_template('index.html', stock=stock, errors=errors)
