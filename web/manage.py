from flask_script import Manager, Server
from stockdata import app
import unittest

manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0'))

@manager.command
def test():
    """Runs all tests in the tests/ folder."""
    tests = unittest.TestLoader().discover('tests', pattern='*tests.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
