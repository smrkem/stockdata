from flask_script import Manager, Server
from stockdata import app
import unittest

manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0'))

@manager.command
def test(testtype='all'):
    """Runs all tests in the tests/ folder."""
    test_type = "tests" if testtype is "all" else "tests/{}".format(testtype)
    tests = unittest.TestLoader().discover(test_type, pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
