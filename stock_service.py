from nsepython import equity_history, nsefetch
import pandas as pd
from pandas.core.algorithms import unique
from utility import get_current_date
from stock import Stock
import sqlite3 as sl
import json
from datetime import datetime
from utility import striped_date_format
import itertools

stock_table_columns = ['_id','symbol', 'series', 'open_price', 'high_price', 'low_price', 'closing_price', 'last_price', 'prev_close_price',
                     'total_traded_qty', 'total_traded_value', 'high_52week', 'low_52week', 'total_trades', 'date', 'created_at', 'updated_at']

class StockService:

    @classmethod
    def get_equity_history(cls, symbol,series,start_date,end_date):
        """
        This method fetches the historical data for the given stock symbol.
        :param symbol: ticker symbol
        :param series: 'EQ' for equity, 'BE' for bond
        :param start_date: start date for the historical data
        :param end_date: end date for the historical data
        :return: historical data for the given stock symbol
        """
        try:
            df = equity_history(symbol,series,start_date,end_date)
            df = cls.map_stock_df_columns(df)
            df['date'] = pd.to_datetime(df['date']).dt.date
            df['date'] = pd.to_datetime(df['date']).dt.strftime(striped_date_format)
            df = cls.check_duplidate_sotck_record(df)
            
            # Fill the missing data with previous day's closing price
            # reference: https://stackoverflow.com/questions/38361526/fill-the-missing-date-values-in-a-pandas-dataframe-column
            df['date'] =  pd.to_datetime(df['date'], format=striped_date_format)
            df = df.sort_values(by=['date'], ascending=[True])
            df.set_index('date', inplace=True)
            df = df.resample('D').ffill().reset_index()
            df['date'] = df['date'].dt.strftime(striped_date_format)
            return df
        except Exception as e:
            print(e)
            return None


    @classmethod
    def check_duplidate_sotck_record(cls,stock_df):
        stock_df = stock_df.drop_duplicates(subset=['symbol','date'])
        return stock_df

    @classmethod
    def fetch_stock_price(cls, symbol,series,start_date, end_date):
        print('fetching stock for order: ', symbol)
        try:
            # if any issue with db connection, then fetch data from nse
            con = sl.connect('data/stocks.db')
            cur = con.cursor()
            result = cur.execute("SELECT * FROM stocks WHERE symbol = ?", (symbol,))
            stock_df = pd.DataFrame.from_records(result.fetchall(), columns=stock_table_columns)
            stock_df['date'] = pd.to_datetime(stock_df['date']).dt.strftime(striped_date_format)
        except Exception as e:
            print(e)
            df = cls.get_equity_history(symbol,series,start_date,end_date)
            return df
        
        # if misisng min or max date, then fetch the data from nse
        if stock_df.empty:
            df = cls.get_equity_history(symbol,series,start_date,end_date)
            return df

        max_date_dt = pd.to_datetime(stock_df['date'], format = "%d-%m-%Y").max()
        min_date_dt = pd.to_datetime(stock_df['date'], format = "%d-%m-%Y").min()
        start_date_dt = datetime.strptime(start_date, "%d-%m-%Y")
        end_date_dt = datetime.strptime(end_date, "%d-%m-%Y")
        if min_date_dt < start_date_dt and max_date_dt > end_date_dt:
        # todo: mask and return the data only between start_date and end_date
            # todo: filter
            stock_df = cls.check_duplidate_sotck_record(stock_df)
            return stock_df
        elif min_date_dt > start_date_dt:
            end_date = min_date_dt.strftime(striped_date_format)
        elif max_date_dt < end_date_dt:
            start_date = max_date_dt.strftime(striped_date_format)
        # todo: fetch only the required data from nse and append to the existing data
        df = cls.get_equity_history(symbol,series,start_date,end_date)
        return df

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
        stock_df.to_sql('stocks', con, if_exists='replace', index=False)


    @classmethod
    def create_stock_from_orders(cls, orders):
        for each_order in orders:
            # create stock object for each order
            start_date = each_order.order_date
            end_date  = get_current_date()
            stock = Stock(each_order.symbol, each_order.series, start_date, end_date)
            # only storing EQ series for now
            if stock.series != 'EQ':
                print('skipping stock: ', stock.symbol, 'series: ', stock.series)
                continue
            stock_price = cls.fetch_stock_price(each_order.symbol,each_order.series,start_date, end_date)
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
                                 'CH_TOTAL_TRADES' : 'total_trades','CH_TIMESTAMP': 'date',
                                  'createdAt': 'created_at', 'updatedAt' : 'updated_at'
                                  }, inplace=True)

        return stock_df

    @classmethod
    def calculate_avg(cls, quantity_price_list):
        total = 0
        count = 0
        if not quantity_price_list:
            return 0
        quantity_price_list = json.loads(quantity_price_list)
        #remove buy and sell of same date from the list
        # altering unrequired avg price of 
        index = 0
        date_order = {}
        filter_index = [1] * len(quantity_price_list)
        updated_quantity_price_list = quantity_price_list.copy()
        for i in quantity_price_list:
            each_date = i.get('date')
            if each_date not in date_order.keys():
                date_order[each_date] = {}
                date_order[each_date]['index'] = filter_index.copy()
            update_index = date_order.get(each_date,{}).get('index').copy()
            update_index[index] = 0
            date_order[each_date]['index'] = update_index
            if i['quantity'] > 0:
                update_quantity = date_order.get(each_date,{}).get('buy_quantity',0) + i['quantity']
                date_order[each_date]['buy_quantity'] = update_quantity 
            elif i['quantity'] < 0:
                update_quantity = date_order.get(each_date,{}).get('sell_quantity',0) + i['quantity']
                date_order[each_date]['sell_quantity'] = update_quantity
            index += 1
        # check and remove
        for each_date in date_order.keys():
            each_date_order = date_order.get(each_date)
            if 'sell_quantity' in each_date_order.keys() and 'buy_quantity' in each_date_order.keys() and \
                abs(each_date_order['buy_quantity']) == abs(each_date_order['sell_quantity']):
                updated_quantity_price_list.clear()
                # for each_index in each_date_order.get('index'):
                #     quantity_price_list.pop(each_index)
                # pick only required columns
                # https://stackoverflow.com/questions/3179106/python-select-subset-from-list-based-on-index-set/3179138#3179138
                for i in itertools.compress(quantity_price_list, each_date_order.get('index')):
                    updated_quantity_price_list.append(i)
                quantity_price_list = updated_quantity_price_list
        for each_quantity_price in quantity_price_list:
            total += each_quantity_price['price']*each_quantity_price['quantity']
            count += each_quantity_price['quantity']
        if count == 0:
            return 0
        avg_price = total/count
        return avg_price

    @classmethod
    def total_quantity(cls, quantity_price_list):
        count = 0
        if not quantity_price_list:
            return 0
        quantity_price_list = json.loads(quantity_price_list)
        for each_quantity_price in quantity_price_list:
            count += each_quantity_price['quantity']
        return count

    @classmethod
    def merge_json_col(cls, row, first_col, sec_col):
        # todo: improve
        if not row[first_col] or row[first_col] == '' or str(row[first_col]) == 'nan':
            first_json_list = []
        else:
            first_json_list = json.loads(row[first_col])
            #todo: improve
        if not row[sec_col] or  row[sec_col] == '' or str(row[sec_col]) == 'nan':
            sec_json_list = []
        else:
            sec_json_list = json.loads(row[sec_col])
        return json.dumps(first_json_list + sec_json_list)

    @classmethod
    def update_price_quantity(cls, each_order, stock_df):
        """
        method will create a column for each symbol.That will contain avg price and quantity
        """
        new_col = each_order.symbol + "_price_quantity"
        order_date = datetime.strptime(each_order.order_date, striped_date_format)
        stock_df['date'] = pd.to_datetime(stock_df['date'],format=striped_date_format)
        #crete a json to store order price and order quantity
        order_price = each_order.price
        order_quantity = each_order.quantity
        order_date = each_order.order_date
        if each_order.order_type == 'buy':
            price_json_list = [{'date' : order_date, 'price': order_price, 'quantity': order_quantity}]
        elif each_order.order_type == 'sell':
            price_json_list = [{'date' : order_date,'price': order_price, 'quantity': -order_quantity}]

        if new_col not in stock_df.columns:
            stock_df[new_col] = None
            stock_df[new_col] = stock_df[new_col].astype(object)
            stock_df.loc[stock_df['date'] >= order_date, new_col] = json.dumps(price_json_list)
            stock_df[each_order.symbol + "_value"] = stock_df[new_col].apply(cls.calculate_avg)
            stock_df[each_order.symbol + "_quantity"] = stock_df[new_col].apply(cls.total_quantity)
            stock_df['date'] = stock_df['date'].dt.strftime(striped_date_format)
            return stock_df
        else:
            stock_df.loc[stock_df['date'] >= order_date, 'temp'] = json.dumps(price_json_list)
            stock_df['temp'].fillna('',inplace=True)
            # stock_df.loc[stock_df['date'] >= order_date].apply( lambda row : cls.merge_json_col(row, new_col, 'temp'))
            stock_df[new_col] = stock_df.apply( lambda row : cls.merge_json_col(row, new_col, 'temp'),axis = 1)
            stock_df.drop(columns = ['temp'], inplace = True)
            stock_df[each_order.symbol + "_value"] = stock_df[new_col].apply(cls.calculate_avg)
            stock_df[each_order.symbol + "_quantity"] = stock_df[new_col].apply(cls.total_quantity)
            stock_df['date'] = stock_df['date'].dt.strftime(striped_date_format)
            return stock_df

    @classmethod
    def calculate_profit_loss_df(cls, orders):
        """
        Create a df with index as date and column as symbol and for each row calculate profit/loss.
        """
        value_index = 'closing_price'
        profit_loss_df = pd.DataFrame({'date' : []})
        for each_order in orders:
            if each_order.series == 'EQ':
                stock_price = cls.fetch_stock_price(each_order.symbol, each_order.series, each_order.order_date, get_current_date())
                stock_price = stock_price[['date', value_index]]
                profit_loss_df = profit_loss_df.merge(stock_price,on = 'date', how = 'outer')
                # merge if symbol's data is present, rename that to old
                if each_order.symbol in profit_loss_df.columns:
                    profit_loss_df.rename(columns={each_order.symbol : each_order.symbol + '_old'}, inplace = True)
                profit_loss_df.rename(columns={'date':'date', value_index: each_order.symbol}, inplace=True)
                # copy the data from old column to new column
                if each_order.symbol + "_old" in profit_loss_df.columns:
                    profit_loss_df.loc[profit_loss_df[each_order.symbol].isnull(), each_order.symbol] = profit_loss_df[each_order.symbol + '_old']
                    profit_loss_df.drop(columns = [each_order.symbol + '_old'], inplace = True)
                profit_loss_df = cls.update_price_quantity(each_order, profit_loss_df)
                if each_order.symbol + "_profit" in profit_loss_df.columns:
                    profit_loss_df.drop(columns=[each_order.symbol + "_profit"],inplace=True)
                profit_loss_df[each_order.symbol + "_profit"] = profit_loss_df[each_order.symbol] * profit_loss_df[each_order.symbol + "_quantity"] - profit_loss_df[each_order.symbol + "_value"] * profit_loss_df[each_order.symbol + "_quantity"]
        # profit_loss_df.set_index('date', inplace=True)
        profit_col = profit_loss_df.columns.str.contains('_profit')
        profit_loss_df['day_profit_status'] = profit_loss_df.loc[:, profit_col].sum(axis=1)
        profit_loss_df['day_profit_status'] = profit_loss_df['day_profit_status'].fillna(0)
        #convert date column
        profit_loss_df['date'] = pd.to_datetime(profit_loss_df['date'], format = striped_date_format)
        profit_loss_df.sort_values(by=['date'], inplace=True)
        # profit_loss_df['profit'] = profit_loss_df['day_profit_status'].cumsum()
        profit_loss_df['daily_profit_and_loss'] = profit_loss_df['day_profit_status'].diff().fillna(profit_loss_df['day_profit_status'])
        # profit_loss_df.to_csv('profit_loss_df.csv',index=False)
        return profit_loss_df

