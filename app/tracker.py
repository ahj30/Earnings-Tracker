# tracker.py
import requests
import json
from datetime import datetime
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import csv

load_dotenv()

ticker_error = 'Ticker not found! Please try again.'
request_error = 'Web Request error! Please try again'
filings_error = 'Error occurred while gathering historical data! Please try again.'
sizing_error = 'Error occurred while compiling historical data!'

def lines():
    print('--------------------------------------------------')

def to_usd(price):
    '''
    Accepts a numeric parameter and converts to USD format 
    Example: to_usd(1234.567) = $1,234.57
    '''
    return '${:,.2f}'.format(price)

def to_percent(ret):
    '''
    Converts decimal returns to standard percent format
    Example: to_percent(.05678) = 5.68%
    '''
    return "{0:.2%}".format(ret)

def verify_ticker(ticker):
    '''
    References Alpha Vantage to make sure ticker has valid stock price data
    No effect on output if successful but exits program if ticker is not found
    '''
    API_KEY = os.getenv("ALPHA_KEY", default = 'break')
    p_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={API_KEY}'
    p_response = requests.get(p_url)
    p_parsed = json.loads(p_response.text)
    if any(z.isdigit() for z in ticker):
        return ticker_error
    elif 'Error Message' in p_parsed:
        return ticker_error
    else:
        return 'Valid ticker identified! . . .'

def verify_web_requests(ticker):
    '''
    Send web requests to websites that will be called in functions below
    Pass if all 3 requests are successful, else exit program
    '''
    next_url = f'https://finance.yahoo.com/calendar/earnings?symbol={ticker}'
    next_response = requests.get(next_url)
    past_url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10&dateb=&owner=exclude&count=40'
    past_response = requests.get(past_url)
    API_KEY = os.getenv("ALPHA_KEY", default = 'break')
    p_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={API_KEY}'
    p_response = requests.get(p_url)
    output = f'{next_response} {past_response} {p_response}'
    if output.count('200') == 3:
        return 'Web Requests fulfilled successfully! . . .'
    else:
        return request_error
        
def get_next_date(ticker):
    '''
    Access Yahoo Finance stock earnings calendar page to request Next Earnings Date
    Return next expected earnings reporting date as YYYY-MM-DD
    '''
    next_url = f'https://finance.yahoo.com/calendar/earnings?symbol={ticker}'
    next_df = pd.read_html(next_url)
    next_date = next_df[0]['Earnings Date'][3]
    next_date = next_date.split(' ')
    del next_date[-2:]
    next_date = ' '.join(next_date)
    next_date = datetime.strptime(next_date, "%b %d, %Y,")
    next_date = datetime.strftime(next_date, '%Y-%m-%d')
    return next_date

def get_past_dates(ticker):
    '''
    Access SEC Edgar database of public financial statements
    Retrieve previous earnings dates and return in Pandas DataFrame form
    '''
    past_url = f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10&dateb=&owner=exclude&count=40'
    past_data = pd.read_html(past_url)
    if len(past_data) > 2:
        df = pd.DataFrame(past_data[2]['Filing Date'])
        return df
    else:
        return filings_error

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

def get_52w_range(JSON_object):
    '''
    Calculates 52-week range from Alpha Vantage API data 
    '''
    closes = []
    high_prices = []
    low_prices = []
    for elm in JSON_object.values():
        high_prices.append(elm['2. high'])
        low_prices.append(elm['3. low'])
        closes.append(elm['4. close'])
    high_prices = [float(x) for x in high_prices[:252]]
    low_prices = [float(x) for x in low_prices[:252]]
    last_close = [float(x) for x in closes[:1]]
    high = to_usd(max(high_prices))
    low = to_usd(min(low_prices))
    last_close = to_usd(last_close[0])
    return f'{low} -- {last_close} -- {high}'

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
    Ensures that dates and prices are correctly aligned before creating DF
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
    if len(closing_prices) == len(returns) == len(df1):
        df1['Closing Price'] = closing_prices
        df1['3d Return'] = returns
        df1.loc[-1] = [next_date, 'NEXT', 'DISCLOSURE']
        df1.index += 1
        df1.sort_index(inplace=True) 
        return df1
    else:
        return sizing_error

def get_return_stats(df1):
    '''
    Generate descriptive statistics of 3-day returns 
    Must remove 'next disclosure' string
    '''
    data = df1.iloc[:,2]
    data1 = data.to_list()
    data1 = [float(x.strip('%')) for x in data1 if x!='DISCLOSURE' and x!='nan%']
    data2 = pd.DataFrame(data1)
    data2.columns = ['3d Return Statistics']
    stats = data2.describe().loc[['mean','std','min','25%','50%','75%','max']]
    stats = stats.iloc[:,0].to_list()
    stats = [to_percent(float(r)/100) for r in stats]
    data3 = pd.DataFrame(stats, index=['Mean','Std Dev','Min','25%','Median','75%','Max'])
    data3.columns = ['3d Return']
    return data3

if __name__ == "__main__":
    print("Welcome to the Earnings Tracker! Stock tickers cannot include numbers or be longer than five characters.")
    ticker = input('Please input a stock ticker: ')
    ticker = ticker.upper()
    lines()
    print(f'Earnings tracker: {ticker}. Please be patient while we gather your information!')

    print(verify_ticker(ticker))
    if verify_ticker(ticker) == ticker_error:
        exit()

    print(verify_web_requests(ticker))
    if verify_web_requests(ticker) == request_error:
        exit()

    print(f'PREPARING DATA ON {ticker} EARNINGS REPORTING . . .')
    lines()
    df = get_past_dates(ticker)
    if type(df) == str:
        print(df)
        print('Make sure to use a company that files quarterly reports with the S.E.C.')
        exit()
    next_date = get_next_date(ticker)
    prices_json = get_prices(ticker)
    prices_df = get_price_df(prices_json)
    df = concat_dfs(df,prices_df)
    if type(df) == str:
        print(df)
        print('There appears to be a data discrepancy between earnings dates and pricing!')   
        print(f'If you have reason to believe {ticker} has gaps in its history as a public company (like DELL or LEVI), please try a different company.') 
        exit()
    print(f'{ticker} 52-week trading range (low, last close, high): {get_52w_range(prices_json)}')
    lines()
    print(df)
    lines()
    print(f'Descriptive statistics for {ticker} earnings date returns:')
    print(get_return_stats(df))
    lines()
