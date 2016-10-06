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
No idea if that will work out ok - when will I learn my lesson? Here's the going vesion of the `web` container's structure.
```
web
├── Dockerfile
├── acceptance_tests
│   └── acceptance_tests.py
├── config.py
├── requirements.txt
├── run.py
└── stockdata
    ├── __init__.py
    └── views.py
```

But the refactor is working fine, and during my poking around and sidetrips, I discovered the `--reload` flag that can be
passed to gunicorn starting command. it's like magic. So finally, a first semi-useful passing FT and a first attempt
at a decent app structure.

```
root@b1b67c5ee175:/usr/src/app# xvfb-run python acceptance_tests/acceptance_tests.py
.
----------------------------------------------------------------------
Ran 1 test in 2.220s

OK
root@b1b67c5ee175:/usr/src/app#
```

Man - that's still feels like an ugly way to run the tests.

<<<<<<< HEAD
Here's the refactoring merge diff -
https://github.com/smrkem/docker-flask-tdd/pull/3/files

(and I very nearly remembered to do everything right to not include the doc updates in the diff :))

****
## Building The StockData App
The app i'm building is going to be a simple, database-driven was for me to keep track of the stocks I'm interested in.
I recently got interested in the stock market - but aside from that I think this'll give a great opportunity to explore
some key areas:
- user system and auth
- a couple basic models
- a few simple forms
- potentially some data collection with api integration / scraping down the line


### Templates and Views
First real development task is to create some views and start using proper templates -
probably with the obligatory bootstrap libraries.

How the hell do I write a test for that?

I don't want to go checking for any specific strings in the template - our current passing FT isn't great.
In django there was a lovely `assert_template_used('template name')`. Turns out, Flask has something similar,
but with the catch that I'd also need to install flask-testing.

## GRRRrrrr
So i need a much better handle on the whole container ecosystem. Currently the tests are running against the gunicorn site.
I don't know exactly what effect that is going to have, but I've been banging my head against Flask's contexts lately,
so for now the simpler the better.

I'm going to try just replacing the web container's run command in the `docker-compose.yml` file with something to just run
the Flask app.

