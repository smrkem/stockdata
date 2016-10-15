### My First Use Case
I am going to start with a use case that is pretty common for me, and one which I happen to be facing at the moment.  

I want to find a US Stock to invest in. My starting criteria is:  
- NASDAQ or NYSE exchange
- price < $4.20  

I ran this basic screener on my online broker account, including the filter Sector & Industry: Telecommunications.  There were 17 results - and I was able to download a csv.  


I'll start my app using this list as my first source of data.  
My thinking is that the app will likely end up querying a 'somthing' and getting back one or more 'Stock' objects. That something might be a file, the app's own db, an external service or whatever.  

I'm also not even considering what a Stock object should look like, (or even for sure that one should exist) at this point.  

What would be useful I think, is if I could input a stock symbol (and exchange?) and get back some useful information.  
- current price
- company information
- trend data
- competitor info
