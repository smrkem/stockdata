### Getting the first FT in shape

This next part feels like it's gonna be a lot of flask docs and tutorials. Bound to be
some refactoring involved. Hope so. So I wanna make sure my first FT is passing and checking
something meaningful.

Currently have:
```
def test_test_is_running(self):
    self.browser = wd.Firefox()
    self.browser.implicitly_wait(3)
    self.browser.get(LIVE_SERVER_URL)
    print(self.browser.page_source)
    print("please?...")
    self.browser.quit()

    print("++++++WORKING!!!+++++")
    self.assertEqual(5, 2)
```

After some quick refactoring, and some long sidetracks on python regex, that becomes:
```
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = wd.Firefox()
        self.browser.implicitly_wait(3)
        pass

    def tearDown(self):
        self.browser.quit()
        pass

    def test_test_is_running(self):
        self.browser.get(LIVE_SERVER_URL)
        self.assertRegex(self.browser.page_source, r'^<html(.*)</html>$')
```
