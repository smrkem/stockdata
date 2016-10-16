from flask import render_template, request
from stockdata import app

@app.route('/', methods=['GET', 'POST'])
def index():
    stock = None
    if request.method == 'POST':
        stock = {'name': 'American Electric Technologies Inc'}
    return render_template('index.html', stock=stock)
