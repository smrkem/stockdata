from flask_script import Manager
from stockdata import app
import unittest

manager = Manager(app)

if __name__ == '__main__':
    manager.run(debug=True, host='0.0.0.0')
