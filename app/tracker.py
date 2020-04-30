# tracker.py
import requests
import json
from datetime import datetime
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

def to_usd(price):
    '''
    Accepts a numeric parameter and converts to USD format 
    Example: to_usd(1234.567) = $1,234.57
    '''
    return '${:,.2f}'.format(price)

def to_percent(ret):
    '''
    Converts decimal returns to standard format
    Example: to_percent(.05678) = 5.68%
    '''
    return "{0:.2%}".format(ret)

def get_web_requests(ticker):
    '''
    Send web requests to websites that will be called in functions below
    Return request status 
    '''
    next_url = f'https://finance.yahoo.com/calendar/earnings?symbol={ticker}'
    next_response = requests.get(next_url)
    past_url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10&dateb=&owner=exclude&count=40'
    past_response = requests.get(past_url)
    API_KEY = os.getenv("ALPHA_KEY", default = 'break')
    p_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={API_KEY}'
    p_response = requests.get(p_url)
    return f'{next_response} {past_response} {p_response}'

def get_next_date(ticker):
    '''
    Access Yahoo Finance stock earnings calendar page to request Next Earnings Date
    Return next expected earnings reporting date as YYYY-MM-DD
    '''
    next_url = f'https://finance.yahoo.com/calendar/earnings?symbol={ticker}'
    next_df = pd.read_html(next_url)
    next_date = next_df[0]['Earnings Date'][3]
    next_date = datetime.strptime(next_date, "%b %d, %Y, %I %p%Z")
    next_date = datetime.strftime(next_date, '%Y-%m-%d')
    return next_date

def get_past_dates(ticker):
    '''
    Access SEC Edgar database of public financial statements
    Retrieve previous earnings dates and return in Pandas DataFrame form
    '''
    past_url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10&dateb=&owner=exclude&count=40'
    past_data = pd.read_html(past_url)
    df = pd.DataFrame(past_data[2]['Filing Date'])
    return df

def get_prices(ticker):
    '''
    Access Alpha Vantage API for daily trading price info
    Return 20 years worth of parsed JSON data 
    '''
    API_KEY = os.getenv("ALPHA_KEY", default = 'break')
    p_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={API_KEY}'
    p_response = requests.get(p_url)
    p_parsed = json.loads(p_response.text)
    p_tsd = p_parsed["Time Series (Daily)"]
    return p_tsd

def get_price_df(JSON_object):
    '''
    Make a Pandas DF for closing prices from JSON data
    Use shift function to calculate returns from yesterday-close to tomorrow-close for each date 
    Return Pandas DF with 3 columns: dates, closing prices, and 3-day return
    '''
    p_dict = {}
    for k,v in JSON_object.items():
        p_dict[k] = float(v['4. close'])
    p_df = pd.DataFrame.from_dict(p_dict, orient='index')
    p_df.columns = ['Close']
    p_df['3d Returns'] = np.log(p_df['Close'].shift(1) / p_df['Close'].shift(-1))
    return p_df

def concat_dfs(df1,df2):
    '''
    Add prices and returns from the Prices DF to the Main DF
    Format DF for optimal presentation to user 
    Add next reporting date to first row of Main DF  
    Return Main DF with 3 columns: prior earnings reporting dates, closing price, and 3 day returns
    '''
    closing_prices = []
    returns = []
    for index,row in df1.iterrows():
        for i,r in df2.iterrows():
            if i == row['Filing Date']:
                closing_prices.append(r['Close'])
                returns.append(r['3d Returns'])
    closing_prices = [to_usd(x) for x in closing_prices]
    returns = [to_percent(r) for r in returns]
    df1['Closing Price'] = closing_prices
    df1['3d Return'] = returns
    df1.loc[-1] = [next_date, 'NEXT', 'DISCLOSURE']
    df1.index += 1
    df1.sort_index(inplace=True) 
    return df1

if __name__ == "__main__":
    ticker = input('Please input a stock ticker: ')
    ticker = ticker.upper()
    print('--------------------------------------------------')
    print(f'PREPARING DATA ON {ticker} EARNINGS REPORTING...')
    print('--------------------------------------------------')
    df = get_past_dates(ticker)
    next_date = get_next_date(ticker)
    prices_json = get_prices(ticker)
    prices_df = get_price_df(prices_json)
    df = concat_dfs(df,prices_df)

    print(df)
