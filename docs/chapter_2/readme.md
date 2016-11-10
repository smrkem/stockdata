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



***


***



### A Clearer Picture  
So things are coming into shape. First version of this thing is going to take a stock symbol and exchange (hopefully in dropdown with nice ux) and return some useful information like:
- Revenue history quarterly / annually
- EPS history q / a
- ...  
  
After looking at a couple different API options (yahoo-finance and a possibly discontinued google-finance, oh yeah - and a WolframAlpha thing only briefly but which looks really cool) - it turns out that the most straightforward way of getting that right now will be a simple scrape of Google Finance. 

This leads into all kinds of questions like  
- what happens when Google changes the site layout or functionality?  
- how can something like this be FT'd ?

### Looking ahead


This information can get used to run PASS / FAIL type scenarios against the company, and generate a score.

It'd be nice to have some way to save or bookmark the information - that means users. 


### chapter 2
Google finance can change at any time, or I may find something better down the line - or I may end up needing to additionally grab info from somewhere else. So i'm thinking to define a GoogleFinanceScraper as a kind of 'source'. I might have several such 'sources' as I go on. 

But that's getting ahead of myself. I'm trying not to think so much in terms of objects and classes and instead focus on 
messages, events and relationships.

The view is gonna need all the stock information - but shouldn't know or care where it comes from. It'll send a `get_stock_info, symbol, exchange` message to something, for now i'll call that the StockInfoGetter. The StockInfoGetter will examine the request and decide which 'source' to use. At first that's gonna be easy since there's just the one choice.

