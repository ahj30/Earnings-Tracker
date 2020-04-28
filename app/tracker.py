# tracker.py
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pandas as pd

# ticker = input('Please input a stock ticker: ')
# ticker = ticker.lower()

### Access Yahoo Finance stock summary page to request Next Earnings Date ###
NEXT_url = 'https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch'
NEXT_response = requests.get(NEXT_url)
NEXT_html = BeautifulSoup(NEXT_response.text, 'html.parser')
NEXT_date_loc =NEXT_html.find('td', attrs={'data-test':'EARNINGS_DATE-value'})
next_date = NEXT_date_loc.find('span').text.strip()
print(next_date)

### Access SEC Edgar to request previous earnings dates ###
PAST_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=AAPL&type=10&dateb=&owner=exclude&count=40'
PAST_response = requests.get(PAST_url)
PAST_data = pd.read_html(PAST_url)
df = PAST_data[2]['Filing Date']
print(df)








