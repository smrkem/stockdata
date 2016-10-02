import unittest
from selenium import webdriver as wd

LIVE_SERVER_URL = 'http://localhost:8000/'


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_test_is_running(self):
        self.browser = wd.Firefox()
        self.browser.implicitly_wait(3)
        self.browser.get(LIVE_SERVER_URL)
        print(self.browser.page_source)
        print("please?...")
        self.assertEqual(1, 0)
        self.browser.quit()


if __name__ == '__main__':
    unittest.main()