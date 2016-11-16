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



### 3. Write FT that checks getting 1yr high and current price.
