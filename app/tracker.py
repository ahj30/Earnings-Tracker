# tracker.py
import requests
import json
from datetime import datetime
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

ticker = input('Please input a stock ticker: ')
ticker = ticker.upper()

### Access Yahoo Finance stock summary page to request Next Earnings Date ###
## Should present next expected earnings reporting date as YYYY-MM-DD ##
NEXT_url = f'https://finance.yahoo.com/calendar/earnings?symbol={ticker}'
NEXT_response = requests.get(NEXT_url)
NEXT_df = pd.read_html(NEXT_url)
next_date = NEXT_df[0]['Earnings Date'][3]
next_date = datetime.strptime(next_date, "%b %d, %Y, %I %p%Z")
next_date = datetime.strftime(next_date, '%Y-%m-%d')

### Access SEC Edgar to request previous earnings dates ###
PAST_url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10&dateb=&owner=exclude&count=40'
PAST_response = requests.get(PAST_url)
PAST_data = pd.read_html(PAST_url)
df = pd.DataFrame(PAST_data[2]['Filing Date'])

### Access Alpha Vantage API for daily trading price info ###
API_KEY = os.getenv("ALPHA_KEY", default = 'break')
PRICES_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={API_KEY}'
PRICES_response = requests.get(PRICES_url)
PRICES_parsed = json.loads(PRICES_response.text)
PRICES_tsd = PRICES_parsed["Time Series (Daily)"]

### Make a Pandas DF for closing prices and returns from yesterday-close to tomorrow-close ###
PRICES_dict = {}
for k,v in PRICES_tsd.items():
    PRICES_dict[k] = float(v['4. close'])
PRICES_df = pd.DataFrame.from_dict(PRICES_dict, orient='index')
PRICES_df.columns = ['Close']
PRICES_df['3d Returns'] = np.log(PRICES_df['Close'].shift(1) / PRICES_df['Close'].shift(-1))

### Add closing prices and returns to main DF ###
closing_prices = []
returns = []
for index,row in df.iterrows():
    for i,r in PRICES_df.iterrows():
        if i == row['Filing Date']:
            closing_prices.append(r['Close'])
            returns.append(r['3d Returns'])
df['Closing Price'] = closing_prices
df['3d Return'] = returns

### Add next reporting date to main DF ###
df.loc[-1] = [next_date, 'NAN', 'NAN']
df.index += 1
df.sort_index(inplace=True) 

print(df)
















