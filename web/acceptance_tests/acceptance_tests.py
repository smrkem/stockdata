import unittest
from selenium import webdriver as wd
from flask import template_rendered
from flask_testing import LiveServerTestCase, TestCase

# Path hack.
import sys, os
sys.path.insert(0, os.path.abspath('.'))

from stockdata import app


LIVE_SERVER_URL = 'http://localhost:5000/'


class NewVisitorTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        print('setUP')
        self.browser = wd.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        pass

    # def _add_template(self, app, template, context):
    #     print("MADE IT HERE")
    #     if len(self.templates) > 0:
    #         self.templates = []
    #     self.templates.append((template, context))

    def test_test_is_running(self):
        print("HERE?")
        # print(self.get_server_url())
        response = self.browser.get(LIVE_SERVER_URL)
        # response = self.browser.get(self.get_server_url())
        # self.assertRegex(self.browser.page_source, r'^<html(.*)</html>$')
        # template_rendered.connect(self._add_template)
        # print(self.templates)
        print(response)
        print(type(response))
        self.assert_template_used('index.html')
        self.fail('ok')


if __name__ == '__main__':
    unittest.main()
