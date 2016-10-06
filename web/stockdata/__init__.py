from flask import Flask
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)

from stockdata import views

def create_app(config_module=None):
    appi = Flask(__name__)
    return appi

if __name__ == '__main__':
    app.run()
