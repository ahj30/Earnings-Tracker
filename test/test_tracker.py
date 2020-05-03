## pytest implementation

import pytest
from datetime import datetime
import pandas

from app.tracker import verify_ticker, verify_web_requests, get_next_date, get_past_dates, get_prices, get_price_df

def test_verify_ticker():
    '''
    Test Alpha Vantage server to ensure that valid tickers are accepted 
    Test that a fake ticker or ticker with no pricing data will be declined
    '''
    assert verify_ticker('MSFT') == 'Valid ticker identified! . . .'
    assert verify_ticker('ABCDEFG') == 'Ticker not found! Please try again.'

def test_verify_web_requests():
    '''
    Test ability to make all web requests for a given ticker 
    Status ID of 200 signals successful request
    '''
    assert verify_web_requests('MSFT') == 'Web Requests fulfilled successfully! . . .'

def test_get_next_date():
    '''
    Test that the function output for AAPL is correct 
    Should return a string of a date
    '''
    assert type(get_next_date('AAPL')) == str
    '''
    Should return a future date
    '''
    today = datetime.now()
    assert datetime.fromisoformat(get_next_date('AAPL')) > datetime.now()

def test_get_past_dates():
    '''
    Test that the function output for Facebook's stock is correct 
    Should return a Pandas DF with a date string in each DataFrame cell
    '''
    assert type(get_past_dates('FB')) == pandas.core.frame.DataFrame
    assert type(get_past_dates('FB')['Filing Date'][0]) == str
    '''
    Should return a date that has already passed
    '''
    today = datetime.now()
    assert datetime.fromisoformat(get_past_dates('FB')['Filing Date'][0]) < datetime.now()
    '''
    Should raise an error if company has no Quarterly Reports on file with S.E.C
    '''
    assert get_past_dates('BUD') == 'Error occurred while gathering historical data! Please try again.'

def test_get_prices():
    '''
    Test that the function output for TSLA is correct 
    Should return a JSON formatted dictionary with daily pricing data
    '''
    assert type(get_prices('TSLA')) == dict
    assert '2020-04-29' in get_prices('TSLA').keys()
    assert '4. close' in get_prices('TSLA')['2020-04-29']

def test_get_price_df():
    '''
    The following JSON input is from the Alpha Vantage time series data for GOOG stock 
    Test that the data is properly transformed into a Pandas DF 
    '''
    sample = {
        "2020-04-29": {
            "1. open": "1341.4600",
            "2. high": "1359.9900",
            "3. low": "1325.3400",
            "4. close": "1341.4800",
            "5. volume": "3764617"
        },
        "2020-04-28": {
            "1. open": "1287.9300",
            "2. high": "1288.0500",
            "3. low": "1232.2000",
            "4. close": "1233.6700",
            "5. volume": "2951309"
        },
        "2020-04-27": {
            "1. open": "1296.0000",
            "2. high": "1296.1500",
            "3. low": "1269.0000",
            "4. close": "1275.8800",
            "5. volume": "1600563"
        },
        "2020-04-24": {
            "1. open": "1261.1700",
            "2. high": "1280.4000",
            "3. low": "1249.4500",
            "4. close": "1279.3100",
            "5. volume": "1640394"
        }
    }
    assert type(get_price_df(sample)) == pandas.core.frame.DataFrame
    assert get_price_df(sample).index[0] == '2020-04-29'
    assert len(get_price_df(sample).columns) == 2
    assert get_price_df(sample)['Close'][3] == 1279.31

