# app.py
from flask import Flask
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)

@app.route('/', methods=['GET'])
def index():
    return "Hi Karl..."


if __name__ == '__main__':
    app.run()
