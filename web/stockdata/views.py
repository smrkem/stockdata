from flask import render_template, request
from stockdata import app

@app.route('/', methods=['GET', 'POST'])
def index():
    stockdata = {
        "AETI": {
            "name": "American Electric Technologies Inc",
            "exchange": "NASDAQ"
        },
        "CRNT": {
            "name": "Ceragon Networks Ltd",
            "exchange": "NASDAQ"
        }
    }
    stock = None
    errors = []
    if request.method == 'POST' and request.form['symbol']:
        stock = stockdata.get(request.form['symbol'])
        if stock is None:
            errors.append("Could not find any stock for symbol: '{}'".format(request.form['symbol']))
    return render_template('index.html', stock=stock, errors=errors)
