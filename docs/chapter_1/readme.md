### My First Use Case
I am going to start with a use case that is pretty common for me, and one which I happen to be facing at the moment.  

I want to find a US Stock to invest in. My starting criteria is:  
- NASDAQ or NYSE exchange
- price < $4.20  

I ran this basic screener on my online broker account, including the filter Sector & Industry: Telecommunications.  There were 17 results - and I was able to download a csv.  

[us_under_4-10152016.csv](../data/us_under_4-10152016.csv)  

I'll start my app using this list as my first source of data.  
My thinking is that the app will likely end up querying a 'somthing' and getting back one or more 'Stock' objects. That something might be a file, the app's own db, an external service or whatever.  

I'm also not even considering what a Stock object should look like, (or even for sure that one should exist) at this point.  

What would be useful I think, is if I could input a stock symbol (and exchange?) and get back some useful information.  
- current price
- company information
- trend data
- competitor info

***

All that begins with the ability to input a stock symbol (and maybe an exchange - we'll see) and get back some info. I wrote
a first FT that does just that. Running these tests gives:
```
... selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: {"method":"id","selector":"symbol"} ...
```
perfect.

A quick addition of an input element to my 'index.html' template gets me past that and to
```
AssertionError: 'American Electric Technologies Inc' not found in 'StockData'
```

It'd be easy to get carried away at this point. Flask probably has some decent options for forms and validation and such -
and I could really start digging in to what should happen when the server receives the symbol. But I'm forcing myself to
keep it simple. All I want to do is determine that something has been submitted, and do something in response. For now, I'll
return the hardcoded name.

https://github.com/smrkem/docker-flask-tdd/pull/5

A couple additions to the tests and views files and we're there. Not very compelling, but neither was the FT.
We'll add some more details to the stock info and also test for different symbols.

Here's the agenda:
- write some new tests that check for more details and multiple stocks
- write some code so all tests pass
- refactor the view code so it gets the stock info from an object dependency
- ensure all tests pass
- refactor tests to use mocking / dependency injection so a test doesn't rely on actual stock data source
- refactor tests to look for a better defined 'stock' on the page (instead of currently just asserting info is in the page_source)
- refactor front-end code to match so all tests are back to passing

### The Double Loop
No idea if I'm using terminology correctly here - bear with me. This is 'outside-in' development. We start with testing the outer
user experience in our FTs. This is the outer loop and leads nicely into the inner, unit-testing loop.

Some failing FTs: https://github.com/smrkem/docker-flask-tdd/commit/eb2d1d13b8870affbb9b48529d5d479b1442e8dc

and now I move on the the unit tests. Instead of adding a new unit test for each property I want to check for,
`test_posting_symbol_returns_stock_name`, `test_posting_symbol_returns_stock_exchange`, ... All i really wanna do
is check that the response contains a stock info object.
```
def test_posting_symbol_returns_stock_info(self):
    response = self.client.post('/', data={'symbol': 'AETI'})
    stock = {
        "name": "American Electric Technologies",
        "exchange": "NASDAQ"
    }

    self.assertEqual(response.status_code, 200)
    self.assertEqual(self.get_context_variable('stock'), stock)
```
which gives: [test output](../test_messages/message_01.txt))

****
Aside: popping in the command I use to create that here for easy reference:
```
stockdata-run-tests >> docs/message_01.txt 2>&1
```
****

I've still got that failing FT at the top, but that's good. Getting my unit tests to pass gets me a little farther in my FT.
I straight-up copy and paste the tests definition of `stock` into the view, add a new variable to the template and I get:
```
AssertionError: 'Ceragon Networks Ltd' not found in '<html ...>'
```
https://github.com/smrkem/docker-flask-tdd/commit/34b5e3d6c04d70ecd83fe3338a30d210351de7ae



We want to be returning the info for the stock symbol that gets POSTed - which means having some way of looking up the stock symbol.
This data might eventually come from anywhere - ideally an external service unless I want a gigantic database that's impossible
to keep up to date.

If the view can pass a `get_stock` message to some object and get back something decent, we'll have what we need -
hopefully in a smart and future-proof way. Time to add a new FT and unit test.

First the FT:
```
# Jim tries to enter some junk to see if the app breaks
        inputbox = self.browser.find_element_by_id("in_symbol")
        inputbox.send_keys("INVALID")
        inputbox.send_keys(Keys.ENTER)

        self.assertIn("Could not find any stock for symbol: 'INVALID'",
                      self.browser.page_source)
```
which yields:
```
AssertionError: "Could not find any stock for symbol: 'INVALID'" not found in '<html ...'
```

Now in to the unit tests - I'll check to see if there's an errors object in the response, and if so I'll print them out.
```
def test_posting_invalid_symbol_returns_error(self):
    response = self.client.post('/', data={'symbol': 'not-valid'})
    errors = ["Could not find any stock for symbol: 'not-valid'"]
    self.assertEqual(self.get_context_variable('errors'), errors)
```
which fails, telling me what to do next:
```
flask_testing.utils.ContextVariableDoesNotExist
```

Again, I'm deliberately keeping things dead simple. Initially, my data source is that 1 limited csv file - from which I
just chose 2 to test against. Using that as a base, I want to build something easy to fix up and extend. For now, those 2
samples just become a python dict keyed off the stock symbol.

The new view looks like so:
```
@app.route('/', methods=['GET', 'POST'])
def index():
    stockdata = {
        "AETI": {
            "name": "American Electric Technologies Inc",
            "exchange": "NASDAQ"
        }
    }
    stock = None
    errors = []
    if request.method == 'POST':
        stock = stockdata["AETI"]
        if stock is None:
            errors.append("Could not find any stock for symbol: 'not-valid'")
    return render_template('index.html', stock=stock, errors=errors)
```
but the error test is still failing:
```
AssertionError: Lists differ: [] != ["Could not find any stock for symbol: 'not-valid'"]
```
since of course the lookup is still hardcoded in and always passes. Looking back at the `index.html` template, I named the
input `symbol` (and the id `in_symbol` - the 'in_' denoting an input - which was a friggin' guess. It might be a good idea to
denote form inputs like that for javascript...)

I have no idea at this point how to go looking into the POST data - instead of googling I'll just debug the `request` object
right from the view and run the tests. I add `print(dir(request)` to see what it responds to and run the test. After more
trial-and-error than I'd like to admit, the view gets to:
```
def index():
    stockdata = {
        "AETI": {
            "name": "American Electric Technologies Inc",
            "exchange": "NASDAQ"
        }
    }
    stock = None
    errors = []
    if request.method == 'POST' and request.form['symbol']:
        stock = stockdata.get(request.form['symbol'])
        if stock is None:
            errors.append("Could not find any stock for symbol: {}".format(request.form['symbol']))
    return render_template('index.html', stock=stock, errors=errors)
```
It wasn't obvious to me that I should use the `.get` method on the stubbed `stockdata` data source. Indexing directly into
the dict with an improper key, threw an exception instead of just returning None - which caused my tests to fails in a truly
frightening way.
[test output](../test_messages/message_03.txt))


but now just the FT is failing. I'm not yet displaying the errors in the page. After a little
```
{% for error in errors %}
  {{ error }}<br>
{% endfor %}
```
in the template, the next FT is failing where we expect:
```
AssertionError: 'Ceragon Networks Ltd' not found in '<html ...'
```
(and in the '...' of that error message is contained my "Could not find any stock for symbol: 'CRNT'" that I was hoping for!
The template is super ugly and bare-bones at this point, but that's pretty much the last item on my ToDo list.

Getting the rest of the tests to pass should be a simple matter of adding that other stock to my faked out data source.
```
stockdata = {
    "AETI": {
        "name": "American Electric Technologies Inc",
        "exchange": "NASDAQ"
    },
    "CRNT": {
        "name": "Ceragon Networks Ltd",
        "exchange": "NASDAQ"
    }
}
```
```
Ran 4 tests in 2.819s

OK
```
Sweeeeeeeeet!

### 3. Refactor the view code so it gets the stock info from an object dependency

With all tests passing it's time to do some refactoring. I'll create a new file in the `stockdata` app called
`services.py` - the idea being that it'll have a StockData object whose job it will be to return stock info for
a passed symbol.

Ordinarily I'd start by writing unit tests for the new class, but it will likely end up being a wrapper for external
requests - and I have no idea what it should look like yet. There is still huge benefit to refactoring now though. It'll
let me get existing tests independant of that future, unknown dependency.

```
class StockData:

    def __init__(self):
        self.stockdata = {
            "AETI": {
                "name": "American Electric Technologies Inc",
                "exchange": "NASDAQ"
            },
            "CRNT": {
                "name": "Ceragon Networks Ltd",
                "exchange": "NASDAQ"
            }
        }

    def get_stock_info(self, symbol):
        return self.stockdata[symbol]
```

and the view becomes:
```
...
from stockdata.services import StockData

@app.route('/', methods=['GET', 'POST'])
def index():
    stock = None
    errors = []
    if request.method == 'POST' and request.form['symbol']:
        stock = StockData().get_stock_info(request.form['symbol'])
        if stock is None:
            errors.append("Could not find any stock for symbol: '{}'".format(request.form['symbol']))
    return render_template('index.html', stock=stock, errors=errors)
```

Running the tests after these changes still gives
```
----------------------------------------------------------------------
Ran 4 tests in 2.864s

OK
```
Fantastic! Here's the current ToDo list:
- ~write some new tests that check for more details and multiple stocks~
- ~write some code so all tests pass~
- ~refactor the view code so it gets the stock info from an object dependency~
- ~ensure all tests pass~
- refactor tests to use mocking / dependency injection so a test doesn't rely on actual stock data source
- refactor tests to look for a better defined 'stock' on the page (instead of currently just asserting info is in the page_source)
- refactor front-end code to match so all tests are back to passing






### The POC Spike

I had hoped to get a lot of Test Driven Development done before taking another detour - I mean the whole getting docker set up
properly for testing was serious effort. But the truth is I started this without a clear idea of what it should be. I'm pretty new
stocks and what data would be useful, as well to the tech side and what sort of data and services is available.

This is honestly a really cool and exciting part for me - I'll put TDD and specific requirements aside for now. A quick
Google for available services and a brand new git branch (`poc/yahoo-finance`) later and I'm ready to explore.

