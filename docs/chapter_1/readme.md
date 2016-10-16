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


