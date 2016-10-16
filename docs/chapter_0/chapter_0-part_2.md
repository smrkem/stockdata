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

```
web:
  restart: always
  build: ./web
  ports:
    - "5000:5000"
  links:
    - postgres:postgres
  volumes:
    - ./web:/usr/src/app
  env_file: .env
  command: python run.py
```

And I just entirely ditched the nginx container for now. I also had to change the `ports` so I could visit my app from local,
and got rid of the `expose`.

Here's the merge: https://github.com/smrkem/docker-flask-tdd/pull/4

- Forgot to update the pip requirements.txt file :(

Everything's working well. Turns out I was kinda testing the wrong thing we selenium. That should be for user-acceptance tests
and should have no knowledge about the server code or implementation.

Testing a certain template was called is definitely more of a unit test for a views thing. So after some refactoring

(https://github.com/smrkem/docker-flask-tdd/commit/f2eaff564b032f6ad3b464734f49e2749f7507d7)

things are finally starting to make decent sense. There's still some ugly importing and organization, but definitely
closing in on something better.

***

After some configuration and playing around, I feel i have a good base to start building the app.

The application itself is organized as a package named stockdata:
```
.
├── acceptance_tests
│   └── acceptance_tests.py
├── config.py
├── requirements.txt
├── run.py
└── stockdata
    ├── __init__.py
    ├── templates
    │   └── index.html
    └── views.py
```
and I can whip the whole thing up with:
```
docker-compose up -d
```

then go into a container to run the tests:
```
docker exec -it stockdata_web_1 /bin/bash
```
and the tests all pass! woot!


### Fixing the Docker test process  
The last thing I want to do is fix up the test running process.  
Currently I'm building the containers, running them in the background, and using `docker exec` to go into the web container to manually run the command.  
```
xvfb-run python acceptance_tests/acceptance_tests.py
```

After some experimenting and false starts, I had issues trying to run `xvfb-run python ...` directly, so I ended up adding a `runtests.sh` script to the web container. Now I can just run
```
docker-compose run --rm web sh /usr/src/app/runtests.sh
```
from my host and the containers will spin up, run the tests putting output to the console, and then go away.  

***

There'll be an opportunity to do some more refactoring of the Flask app to use a manage.py file and a testrunner. Figure
I'll look at that stuff when I attach a db.

This is really the end of setting things up - so I think this is gonna become chapter_0, part 2 or something like that.
I want to start chapter_1 off with some initial FTs that start describing my app.

### Stockdata
(imaginative title - huh?)
It will start off as something to keep track of various equities (stocks) and associated data (exchange, symbol, ...)
including dynamic data like price, volume, market cap, ... stored with its datetime.

One I introduce users, they can have a stock portfolio, total market value, etc.
Can watch certain stocks and set notifications for conditions (can do this in TD)
