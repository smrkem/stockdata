from flask import Flask
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)

from stockdata import views

if __name__ == '__main__':
    app.run()
