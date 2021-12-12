from portfolio import Portfolio
from stock_service import StockService

# create portfolio
portfolio = Portfolio(portfolio_name='my_investment_portfolio')
# load the data
portfolio.load()
# create data
data = StockService.calculate_profit_loss_df(portfolio.order_list)
# plot the data
print(data.shape)
