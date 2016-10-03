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
and voila! Passing tests so on to the refactoring!

I'm pretty new to Flask, so I'll be loosely following Miguel Grinberg's
- http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

In his Hello World - the app is split off into a couple different files. the main app lives as a folder with
an `__init__.py` file, making it a package you can import.

The routes themselves are defined in a separate file - `app/views.py`. I'll be renaming this to routes i think.
I love flask so far, but not so much the views / controllers + templates convention.
- I'm thinking model, view / templates, controller / routes

...


Scratch that. Just tried it out and routes.py definitely doesn't feel right - flipping back to Miguel's way for now.
While I'm up though - what's with that cockeyed mix of what seems to be 2 different uses of `app` in his `app/__init__.py`?
```
app = Flask(__name__)
from app import views
```

I'm gonna try, in my folder structure and packages to replace the more generic app with the actual app's name 'stockdata'.
No idea if that will work out ok - when will I learn my lesson?

But the refactor is working fine, and during my poking around and sidetrips, I discovered the `--reload` flag that can be
passed to gunicorn starting command. it's like magic.

