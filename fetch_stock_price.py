from nsepython import equity_history, nsefetch


def equity_history(symbol,series,start_date,end_date):
    payload = nsefetch("https://www.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22"+series+"%22]&from="+start_date+"&to="+end_date+"")
    # return pd.DataFrame.from_records(payload["data"])
    return payload['data']


def fetch_stock_price(symbol,series,start_date, end_date):
    return equity_history(symbol,series,start_date,end_date)

