import requests
from nsepython import equity_history, nsefetch
import pandas as pd


def equity_history(symbol,series,start_date,end_date):
    payload = nsefetch("https://www.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22"+series+"%22]&from="+start_date+"&to="+end_date+"")
    # return pd.DataFrame.from_records(payload["data"])
    return payload['data']


def fetch_stock_price(symbol,series,start_date, end_date):
    symbol = "DEVYANI"
    series = "EQ"
    start_date = "08-06-2021"
    end_date ="14-12-2021"
    return equity_history(symbol,series,start_date,end_date)


    # """
    # Fetch stock price from Yahoo Finance
    # :param ticker: stock ticker
    # :return: stock price
    # """
    # url = "http://finance.yahoo.com/d/quotes.csv?s={}&f=l1".format(ticker)
    # response = requests.get(url)
    # price = response.text.strip()
    # return float(price)
