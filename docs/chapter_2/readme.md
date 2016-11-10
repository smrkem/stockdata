found this online, which is nice enough to detail the different countries, exchanges and stock symbol suffixes:

http://www.jarloo.com/yahoo_finance/

***

Came across some guy's awesome gist: (locate url - SO?)


want to get company information like
```
GOOGLE_FINANCE_REPORT_TYPES = {
    'inc': 'Income Statement',
    'bal': 'Balance Sheet',
    'cas': 'Cash Flow',
}
```

The idea is to use something like PyQuery

https://pythonhosted.org/pyquery/

to scrape Google Finance urls of the form:

https://www.google.com/finance?q=NEON:NASDAQ&fstype=ii

looks like `fstype=ii` might denote Financials. Haven't messed around with trying different values yet.

When there are no financials for the market and symbol, then the
```
<div id="app" ... <div class="fjfe-content">
```
element will be empty.


***
```
# Jim inputs the symbol "SYMB"
# He sees the page refresh with the 52-week high, 200-day-ave, 50-day-ave and 7-day ave
```

I'm thinking it's gonna be good, in general, to compare how things look at various timescales - maybe get a good picture of where things are headed in the short term.

Gonna do rolling statistics on a year's worth of historical data - like standard deviation (volatility) for 1-year, 200-day, 50-day and 7-day