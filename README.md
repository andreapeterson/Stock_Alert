# Stock_Alert
By incorporating this code into AWS Lambda and setting up SNS and CloudWatch events, every day at 8 a.m. an email will send with 3 relevant news articles if Amazon's stock price difference is greater than 5%.

With this project, I learned that using AWS SNS to send emails is simply just way more efficient than using SMTPLIB in Python. It is simple, easy to set up, and has a very fast response. It is also flexible where you could easily send to multiple subscribers/emails and change them without editing your code. This project also taught me the importance of list comprehension and slicing in Python. Originally, I avoided them and had 5 lines of code for what list comprehension did in 1. List comprehension is something that doesn't come naturally to my mind but it is important in simplifying code so I will continue to study it and use it. 

Important note: I had to change my Lambda's runtime settings to Python 3.7 so that I could use "from botocore.vendored import requests" to request the API's as it does not work on the newer versions of Python. I researched and this was the simplest solution I found, but not the most efficient so I will continue to look into the subject and update code if I find a better way.

I used Amazon but you could put in any stock your interested in keeping up with. Sensitive information in config.py.
