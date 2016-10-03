from stockdata import app

@app.route('/', methods=['GET'])
def index():
    return "Hi FTW..."
