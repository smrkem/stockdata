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

This will lead to all kinds of questions like:

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
4. Write unit tests for the approach
5. Code till unit tests pass, verifying FT passes at the end
6. Add bootstrap to the app so it looks nicer
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


Ultimately I'm gonna want to be able to get info from a list of sources, maybe depending on what's asked for in the query. For now, the minimal thing is for get_stock_info to call the YahooFinanceClient's get_stock_info.

```

class StockDataTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    @patch('stockdata.services.YahooFinanceClient')
    def test_get_stock_info_calls_source_get_stock_info(self, mock_source):
        mock_source.return_value.get_stock_info.return_value = {"stock":"data"}
        stock = StockData()
        stockdata = stock.get_stock_info("SYMB")
        mock_source.return_value.get_stock_info.assert_called_with("SYMB")
        self.assertEqual(stockdata, {"stock":"data"})

```  

A quick bout of inner TDD and my `services.py` becomes:  
```
from stockdata.sources.YahooFinanceClient import YahooFinanceClient


class StockData:

    def get_stock_info(self, symbol):
        return YahooFinanceClient().get_stock_info(symbol)
```
and I've added a new 'sources' folder (with an __init__.py) for the vary basic `sources/YahooFinanceClient.py`:
```
class YahooFinanceClient:

    def get_stock_info(self, symbol):
        pass
```



[test_messages](../test_messages/message_05.txt)


Notice that now my unit tests are all passing, but the FT broke. That's cool - totally expected and I'll know I've done my job right when the FT passes at the end (though it'll likely need some small modifications)  

Now i add some tests for the YahooFinanceClient - just in the same `test_service_clients.py` file. Along the way I get caught up refactoring my services organization. Looking at the diff:  

https://github.com/smrkem/docker-flask-tdd/commit/4301cb91878abbf1ffca5e10e11624ebb6ffe0f3

I'm not at all sure that was a good idea.

...  

I wasn't even done yet. One more commit before the tests are failing in any way that makes sense.  

https://github.com/smrkem/docker-flask-tdd/commit/2559111e474d614fb2443fdecfdb81ee17218857


And the FT is still failing - expected, but kinda noisy. Next up - another detour to let me use Manager to just run unit_tests.  

https://github.com/smrkem/docker-flask-tdd/commit/0d68e8c480407f9dfc2d71091cfb7fa386393022

That was almost fun. A little hacky and unneccessary - but now I can run just the unit tests with
```
docker-compose run --rm web sh runtests.sh unit
```
(which i've aliased to just `tdddocker-run-tests unit`). And i was also able to get rid of that stupid `z_acceptance_tests` folder name too. Now that I can run just the unit tests, don't care a whole lot if the FTs come first. The majority of my time is spent going back and forth between unit tests and coding - in the inner loop.  




_just had to fix the unit test patching_  
_and also wondering if markdown will respect the 4 blank lines i left above this in atom editor (which keeps getting rid of the 2 blank spaces i'm leaving on each empty line - cuz markdown ... who the fuck knows?)



So the unit tests are failing with:  
- [test_messages](../test_messages/message_06.txt)  

```
AttributeError: <module 'stockdata.services.sources.YahooFinanceClient' from '/usr/src/app/stockdata/services/sources/YahooFinanceClient.py'> does not have the attribute 'Share'
```
_(wow. i'm still learning python's module / package import rules, and those long module name chains *really* feels wrong)_

Stuck a
```
from yahoo_finance import Share
```
in there and also added `yahoo-finance` to my requirements.txt (which means i need to do a `docker-compose buld` again). Had to tidy up the codebase a bit too - embarassing :(  



_speaking of embarassing_, the next failure is:  
```
YahooFinanceClient().get_stock_info()
TypeError: 'module' object is not callable
```

Fixing that, and another round of inner TDD, there's new tests and code:

https://github.com/smrkem/docker-flask-tdd/commit/444508bd5530485bfad999533e7db7ab25952974

and the test failure messages that lead to it:


[test_messages](../test_messages/message_07.txt)

The StockData class is not using a YahooFinanceClient 'source' to query yahoo-finance. I know my code is making the right calls, but no idea if yahoo-finance is returning anything that makes sense with what i'm doing - or anything at all.  

For that I go look at how my FTs are doing - which I can run pretty easily now (using my alias) with:
- `tdddocker-run-tests acceptance`

```

======================================================================
FAIL: test_can_visit_homepage (test_getting_stock_info.NewVisitorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/src/app/tests/acceptance/test_getting_stock_info.py", line 47, in test_can_visit_homepage
    self.check_stock_info_for(("AETI", "American Electric Technologies Inc", "NASDAQ"))
  File "/usr/src/app/tests/acceptance/test_getting_stock_info.py", line 30, in check_stock_info_for
    self.assertIn(value, stockinfo_table.text, "Check {} is in stock info".format(value))
AssertionError: 'American Electric Technologies Inc' not found in 'Symbol AETI\nName American Electric Technologies,\nExchange NCM' : Check American Electric Technologies Inc is in stock info

----------------------------------------------------------------------
Ran 1 test in 6.483s

FAILED (failures=1)
```

That's cool. It's calling yahoo-finance with "AETI" and everythings cool - except yahoo is calling the company something slightly different. I haven't looked at that initial `us_under_4` spreadsheet in forever. don't care about it anymore. Yahoo variation works fine there.

I had been struggling with the choice between leaving my acceptance tests to query the actual external service (which is way easier and less hacky) - or attempting to mock its response.  

Decided for now to keep it making actual requests. I don't plan on running my FTs often and repeatedly, and this way I'm testing the whole system.

On my way to fixing the FTs - i encountered this error:  
```
raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: {"method":"id","selector":"errors"}
```

which meant a small refactor to the YahooFinanceClient:
```
def get_stock_info(self, symbol):
    stock = Share(symbol)
    stock_name = stock.get_name()
    if stock_name is None:
        return None

    stock_exchange = stock.get_stock_exchange()
    return {
        "symbol": symbol,
        "name": stock_name,
        "exchange": stock_exchange
    }
```

but other than that, all I needed to do was correct the company names and change the exchange to be whatever those acronyms the yahoo-finance service is returning. Guess I'll get to learn those over time.

All my tests are green:
```
$ tdddocker-run-tests
 * Running on http://127.0.0.1:8943/ (Press CTRL+C to quit)
test_can_visit_homepage (acceptance.test_getting_stock_info.NewVisitorTest) ... ...
ok
test_get_stock_info_calls_source_get_stock_info (unit.test_service_clients.StockDataTest) ... ok
test_get_stock_info_fetches_exchange (unit.test_service_clients.YahooFinanceClientTest) ... ok
test_get_stock_info_fetches_name (unit.test_service_clients.YahooFinanceClientTest) ... ok
test_get_stock_info_gets_share_for_symbol (unit.test_service_clients.YahooFinanceClientTest) ... ok
test_get_stock_info_returns_stock (unit.test_service_clients.YahooFinanceClientTest) ... ok
test_home_view_calls_index_template (unit.test_views.HomeViewTest) ... ok
test_posting_invalid_symbol_returns_error (unit.test_views.HomeViewTest) ... ok
test_posting_symbol_returns_stock_info (unit.test_views.HomeViewTest) ... ok

----------------------------------------------------------------------
Ran 9 tests in 6.482s

OK
```

which feels fantastic. Firing up the server and visiting the app in my browser I have to play around and convince myself it's all good for a while.  
- `docker-compose up -d`


### 3. Write FT that checks getting 1yr high and current price.  
That's all great, but the app still isn't very useful. The whole time i was playing in the browser I was excited thinking about how much more this thing can easily show me.  

Here's the agenda at this point:


***
### Agenda:
1. ~~Refactor project to use Flask Manager (`manage.py`)~~
2. ~~Refactor project to get info from yahoo-finance - Get all tests back to passing~~
3. Write FT that checks getting 1yr high and current price.
4. Write unit tests for the approach
5. Code till unit tests pass, verifying FT passes at the end
6. Add bootstrap to the app so it looks nicer
***

The app can display the stock's current price and 1yr high on the page - seems like a decent idea. But I don't want to test for specific values on those guys. I'm thinking it'll be good to check for numeric values and that's it. I don't even want to check the 1yr high is larger than current price cuz that might not always be true.

My `check_stock_info_for` seems like the best place to do that (and i'll add some structure to my template html to ease the process).
```
def check_stock_info_for(self, stockinfo):
    stockinfo_table = self.browser.find_element_by_id("stock-info")
    for value in stockinfo:
        self.assertIn(value, stockinfo_table.text, "Check {} is in stock info".format(value))
    current_price = stockinfo_table.find_element_by_id("stck-curent-price").text
    year_high = stockinfo_table.find_element_by_id("stck-1yr-high").text
    self.assertTrue(current_price.isdigit())
    self.assertTrue(year_high.isdigit())
```

This may not be the right way to check that - but i guess i'll figure that out when i finish the inner TDD loop. For now the FT fails with
```
Message: Unable to locate element: {"method":"id","selector":"stck-curent-price"}
```
which I can easily remedy with an update to the template, adding :
```
<tr>
  <td>Current Price:</td>
  <td id="stck-curent-price">{{ stock.current_price }}</td>
</tr>
<tr>
  <td>1 Year High:</td>
  <td id="stck-1yr-high">{{ stock.year-high }}</td>
</tr>
```

I leave the outer FT loop, failing with a promising:
```
self.assertTrue(current_price.isdigit())
AssertionError: False is not true
```
and head inwards.

First add some unit tests:
```
@patch('stockdata.services.sources.YahooFinanceClient.Share')
+    def test_get_stock_info_fetches_year_high(self, mock_share):
+        YahooFinanceClient().get_stock_info("SYMB")
+        mock_share.return_value.get_year_high.assert_called_with()
+
+    @patch('stockdata.services.sources.YahooFinanceClient.Share')
+    def test_get_stock_info_fetches_current_price(self, mock_share):
+        YahooFinanceClient().get_stock_info("SYMB")
+        mock_share.return_value.get_price.assert_called_with()
+
+    @patch('stockdata.services.sources.YahooFinanceClient.Share')
def test_get_stock_info_returns_stock(self, mock_share):
    mock_share.return_value.get_stock_exchange.return_value = "TST"
    mock_share.return_value.get_name.return_value = "Test Company Name"
+        mock_share.return_value.get_price.return_value = 2.32
+        mock_share.return_value.get_year_high.return_value = 6.66

    expected_stock = {
        "symbol": "SYMB",
        "name": "Test Company Name",
-            "exchange": "TST"
+            "exchange": "TST",
+            "current_price": 2.32,
+            "year_high": 6.66
    }
    actual_stock = YahooFinanceClient().get_stock_info("SYMB")

```

and then some code to make them pass:
```
class YahooFinanceClient:

    def get_stock_info(self, symbol):
        stock = Share(symbol)
        stock_name = stock.get_name()
        if stock_name is None:
            return None
        stock_exchange = stock.get_stock_exchange()
        current_price = stock.get_price()
        year_high = stock.get_year_high()

        return {
            "symbol": symbol,
            "name": stock_name,
            "exchange": stock_exchange,
            "current_price": current_price,
            "year_high": year_high
        }
```
Perfect. Turns out I need a minor correction to my FTs. Just replacing:
```
self.assertTrue(current_price.isdigit())
self.assertTrue(year_high.isdigit())
```

with
```
self.assertRegexpMatches(current_price, r'^\d+\.\d+')
self.assertRegexpMatches(year_high, r'^\d+\.\d+')]
```
and all my tests are passing. Check out the app in the browser and we're starting to get some actual data. It's a bit of a pain having to figure out the right extension for Canadian stocks (OGI.V, BLO.CN) or probably any non-nassaq / nyse traded stock. Maybe i'll add something to make that easier...


***
### Agenda:
1. ~~Refactor project to use Flask Manager (`manage.py`)~~
2. ~~Refactor project to get info from yahoo-finance - Get all tests back to passing~~
3. ~~Write FT that checks getting 1yr high and current price.~~
4. ~~Write unit tests for the approach~~
5. ~~Code till unit tests pass, verifying FT passes at the end~~
6. Add bootstrap to the app so it looks nicer
***
