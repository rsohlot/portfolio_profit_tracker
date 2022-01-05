import os
import sys
root_folder = os.path.join(sys.path[0],"../").replace("\\","/")
sys.path.append(root_folder)

from portfolio import Portfolio
from prediction.train import train

# create portfolio
portfolio = Portfolio(portfolio_name='my_investment_portfolio')
# load the data
portfolio.load()

unique_symbols = list(set([each_order.symbol for each_order in portfolio.order_list]))
# Train for each order in portfolio
for each_order in portfolio.order_list:
    print('Training for ', each_order.symbol)
    train(symbol= each_order.symbol)