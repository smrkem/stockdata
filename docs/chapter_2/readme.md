### A Clearer Picture

So things are coming into shape. First version of this thing is going to take a stock symbol (and maybe an exchange)
and return some useful information like:
- Revenue history quarterly / annually
- EPS history q / a
- price history stats


I looked into a few apis and options and it seems that in order to get decent company financials like EPS and revenue,
the most straightforward thing to do is scrape a site like GoogleFinance or Yahoo. For price history data the yahoo-finance
python module looks amazing. It will allow me to get the raw data into a pandas dataframe if I want to -
so there's a good chance a little data-analysis might find it's way in here.


##### Future Considerations

This will lead into all kinds of questions like:

- what happens when Google changes the site layout or functionality?
- how can something like this be FT'd ?
- should i be caching data on the server anywhere along the line ?

But I'll try to tackle these as they come. For now I wanna get started.

***

Given all that data, I think it would be cool to run PASS / FAIL tests on stock's current situation.
There's a kind of geeky inception to using TDD to build an app that itself runs other tests. maybe. whatever.

I'm going to start with a simple test:

**is the stock currently trading within 15% of it's 1yr high?**

that is going to mean using the yahoo-finance library. No web scraping just yet.


I'm all finished with my `poc/yahoo-finance` branch for now, but i'm going to keep it around. As I come back
to master and check out the state of my project, I'm seeing something to improve right away.

It's starting to become a hassle to keep sticking all the tests in a single file. It'll be good to look into a testrunner
like nose or maybe a Flask manage.py approach. This'll also allow me to fix up how those tests are structured a bit.



After that things get a little involved. I'm going to be pulling data from yahoo-finance, and my existing service and FT
code is pretty hardcoded. I need to refactor my code to make requests on the external service. My unit tests


I'm going to have to make a choice here:
- Send actual requets to the external yahoo-service during FTs
- Implement some method of 'faking' the response during FTs

So far I'm seeing pros and cons for each.




Here's my todo list (which will probably evolve along the way):

***
### Agenda:
1. Refactor project to use Flask Manager (`manage.py`)
2. Refactor project to get info from yahoo-finance - Get all tests back to passing
3. Write FT that checks getting 1yr high and current price.
2. Plan my approach
3. Write unit tests for the approach
4. Code till unit tests pass, verifying FT passes at the end
5. Add bootstrap to the app so it looks nicer
***

That's the outer loop (FT), inner-loop (unit test) rythym i'm trying to get down.



Here's the diff that gets the Flask Manager approach (using a `manage.py` file) working:

https://github.com/smrkem/docker-flask-tdd/commit/e78bc2b9743202cfdcea689520d90e1b3d485b53


Now that I have test-discovery, I can split up my tests into folders (that apparently need to be modules with an `__init__.py` file?)
and name them a little better. What I had before was gonna get real messy, real quick.

https://github.com/smrkem/docker-flask-tdd/commit/9b5ec1dae8656e95998efae199dceef8e4f31f06


Things are working pretty good - that `z_acceptance_tests` naming was just cuz I like my FTs to run after all the unit tests.


### 2. Refactor project to get info from yahoo-finance - Get all tests back to passing

I'm going to be adding a YahooFinanceClient as 'source' for the StockData class. I start with a new test file for
services and clients `test_service_clients.py`.

https://github.com/smrkem/docker-flask-tdd/commit/f1f79b032186d02792d0ab0b2d94659d9e81e0aa

which fails expectedly:
```

======================================================================
ERROR: test_has_a_list_of_sources (unit_tests.test_service_clients.StockDataTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/src/app/tests/unit_tests/test_service_clients.py", line 16, in test_has_a_list_of_sources
    self.assertIsInstance(stock.sources, type(list()))
AttributeError: 'StockData' object has no attribute 'sources'

======================================================================
FAIL: test_stockdata_format (unit_tests.test_service_clients.StockDataTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/src/app/tests/unit_tests/test_service_clients.py", line 22, in test_stockdata_format
    'Name', 'Exchange', 'Symbol'
AssertionError: dict_keys(['AETI', 'CRNT']) != ['Name', 'Exchange', 'Symbol']

----------------------------------------------------------------------
Ran 6 tests in 2.992s

FAILED (failures=1, errors=1)
```



### 3. Write FT that checks getting 1yr high and current price.




