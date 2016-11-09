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

