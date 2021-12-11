# from os import sync
from nsepython import equity_history, nsefetch
import pandas as pd
from utility import get_current_date
from stock import Stock
import sqlite3 as sl

stock_table_columns = ['_id','symbol', 'series', 'open_price', 'high_price', 'low_price', 'closing_price', 'last_price', 'prev_close_price', 'total_traded_qty', 'total_traded_value', 'high_52week', 'low_52week', 'total_trades', 'date', 'created_at', 'updated_at']
class StockService:
    def equity_history(self, symbol,series,start_date,end_date):
        payload = nsefetch("https://www.nseindia.com/api/historical/cm/equity?symbol="+symbol+"&series=[%22"+series+"%22]&from="+start_date+"&to="+end_date+"")
        # return pd.DataFrame.from_records(payload["data"])
        return payload['data']

    @classmethod
    def fetch_stock_price(cls, symbol,series,start_date, end_date):
        try:
            # if any issue with db connection, then fetch data from nse
            con = sl.connect('data/stocks.db')
            cur = con.cursor()
            result = cur.execute("SELECT * FROM stocks WHERE symbol = ?", (symbol,))
            stock_df = pd.DataFrame.from_records(result.fetchall(), columns=stock_table_columns)
            stock_df['date'] = pd.to_datetime(stock_df['date']).dt.strftime('%d-%m-%Y')
        except Exception as e:
            print(e)
            return equity_history(symbol,series,start_date,end_date)
        
        max_date = stock_df['date'].max()
        min_date = stock_df['date'].min()
        # if misisng min or max date, then fetch the data from nse
        if stock_df.empty:
            return equity_history(symbol,series,start_date,end_date)
        if min_date < start_date and max_date > end_date:
            # todo: mask and return the data only between start_date and end_date
            return stock_df
        elif min_date > start_date and max_date < end_date:
            # todo: fetch only the required data from nse and append to the existing data
            return equity_history(symbol,series,start_date,end_date)
        elif min_date > start_date:
            end_date = min_date
            return equity_history(symbol,series,start_date,end_date)
        elif max_date < end_date:
            start_date = max_date
            return equity_history(symbol,series,start_date,end_date)
        else :
            return equity_history(symbol,series,start_date,end_date)

    @classmethod
    def store_stocks(cls, stock_df):
        con = sl.connect('data/stocks.db')
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS stocks (_id text,symbol text, series text, open_price real, high_price real, low_price real, closing_price real, last_price real, prev_close_price real, total_traded_qty int, total_traded_value real, high_52week real, low_52week real, total_trades int, date date, created_at timestamp, updated_at timestamp)")
        # for stock in stocks:
        #     cur.execute("INSERT INTO stocks VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (stock.symbol, stock.series, stock.open, stock.high, stock.low, stock.close, stock.last, stock.prevClose, stock.totalTradedQty, stock.totalTradedVal, stock.timestamp, stock.isin, stock.date, stock.time, stock.series_name))
        # con.commit()
        # con.close()
        stock_df = stock_df[stock_table_columns]
        stock_df.to_sql('stocks', con, if_exists='append', index=False)


    @classmethod
    def create_stock_from_orders(cls, orders):
        for each_order in orders:
            # create stock object for each order
            print('fetching sotck for order: ', each_order.symbol)
            start_date = each_order.order_date
            end_date  = get_current_date()
            stock = Stock(each_order.symbol, each_order.series, start_date, end_date)
            # only storing EQ series for now
            if stock.series != 'EQ':
                print('skipping stock: ', stock.symbol, 'series: ', stock.series)
                continue
            stock_price = cls.fetch_stock_price(each_order.symbol,each_order.series,start_date, end_date)
            stock_price = pd.DataFrame.from_records(stock_price)
            # change
            stock_price = cls.map_stock_df_columns(stock_price)
            stock_price['date'] = pd.to_datetime(stock_price['date']).dt.date
            stock_price['date'] = pd.to_datetime(stock_price['date']).dt.strftime('%d-%m-%Y')
            stock.set_stock_price(stock_price)
            cls.store_stocks(stock_price)
    
    @classmethod
    def map_stock_df_columns(cls,stock_df):
        stock_df.rename(columns = {'CH_SYMBOL':'symbol','CH_SERIES' : 'series' ,
                                 'CH_TRADE_HIGH_PRICE':'high_price', 'CH_TRADE_LOW_PRICE':'low_price',
                                 'CH_OPENING_PRICE':'open_price','CH_CLOSING_PRICE': 'closing_price' ,
                                  'CH_LAST_TRADED_PRICE':'last_price', 'CH_PREVIOUS_CLS_PRICE':'prev_close_price',
                                  'CH_TOT_TRADED_QTY':'total_traded_qty', 'CH_TOT_TRADED_VAL':'total_traded_value',
                                  'CH_52WEEK_HIGH_PRICE' : 'high_52week', 'CH_52WEEK_LOW_PRICE':'low_52week',
                                 'CH_TOTAL_TRADES' : 'total_trades','TIMESTAMP': 'date',
                                  'createdAt': 'created_at', 'updatedAt' : 'updated_at'
                                  }, inplace=True)

        return stock_df

    @classmethod
    def calculate_avg(cls, qnty_rate_list):
        total = 0
        count = 0
        for each_qnty_rate in qnty_rate_list:
            total += each_qnty_rate['rate']*each_qnty_rate['quantity']
            count += each_qnty_rate['quantity']
        avg_rate = total/count
        return avg_rate

    @classmethod
    def total_qnty(cls, qnty_rate_list):
        count = 0
        for each_qnty_rate in qnty_rate_list:
            count += each_qnty_rate['quantity']
        return count

    @classmethod
    def update_rate_qnty(cls, each_order, stock_df):
        """
        method will create a column for each symbol.That will contain avg rate and qnty
        """
        new_col = each_order.symbol + "_rate_qnty"
        if new_col not in stock_df.columns:
            stock_df[new_col] = None
            stock_df.loc[stock_df.loc['date'] >= each_order.order_date, new_col] = [{'rate': each_order.rate, 'quantity': each_order.qnty}]
            stock_df[each_order.symbol + "_value"] = stock_df[new_col].apply(cls.calculate_avg)
            stock_df[each_order.symbol + "_quantity"] = stock_df[new_col].apply(cls.calculattotal_qntye_avg)
            return stock_df
        else:
            stock_df.loc[stock_df.loc['date'] >= each_order.order_date, new_col] = stock_df[new_col] + [{'rate': each_order.rate, 'qnty': each_order.qnty}]
            stock_df[each_order.symbol + "_value"] = stock_df[new_col].apply(cls.calculate_avg)
            stock_df[each_order.symbol + "_quantity"] = stock_df[new_col].apply(cls.calculattotal_qntye_avg)
            return stock_df

    @classmethod
    def calculate_profit_loss_df(cls, orders):
        """
        Create a df with index as date and column as symbol and for each row calculate profit/loss.
        """
        value_index = 'closing_price'
        profit_loss_df = pd.DataFrame()
        for each_order in orders:
            if each_order.order_type == 'buy':
                stock_price = cls.fetch_stock_price(each_order.symbol, each_order.series, each_order.order_date, get_current_date())
                stock_price = stock_price[['date', value_index]]
                profit_loss_df = profit_loss_df.append(stock_price)
                profit_loss_df.rename(columns={'date':'date', value_index: each_order.symbol}, inplace=True)
                profit_loss_df = cls.update_rate_qnty(each_order, profit_loss_df)
                profit_loss_df[value_index+"_profit"] = profit_loss_df[each_order.symbol + "_value"] * profit_loss_df[each_order.symbol + "_quantity"] - profit_loss_df[value_index] * profit_loss_df[each_order.symbol + "_quantity"]
        profit_loss_df.set_index('date', inplace=True)
        return profit_loss_df

