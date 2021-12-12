import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from utility import striped_date_format

# Fetch data
from portfolio import Portfolio
from stock_service import StockService


def create_portfolio(name):
    # create Dataset
    # create portfolio
    portfolio = Portfolio(portfolio_name='my_investment_portfolio')
    # load the data
    portfolio.load()
    # create data
    data = StockService.calculate_profit_loss_df(portfolio.order_list)
    # plot the data
    print(data.shape)
    return data


data = create_portfolio('my_investment_portfolio')
#convert date column
data['date'] = pd.to_datetime(data['date'], format = striped_date_format)
data.sort_values(by=['date'], inplace=True)
# data['profit'] = data['daily_profit'].cumsum()
# required data
required_cols = ['date']
profit_col = [col for col in data.columns if '_profit' in col]
required_cols.extend(profit_col)

data = data[required_cols]

# graph 
fig = px.line(data, x="date", y=data.columns[1:])
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x")

# App for plotting
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

app.layout = html.Div([
    # graph
     dcc.Graph(figure=fig),
], id='main-div', style = {'display': 'inline-block','height' : '95%', 'width': '95%'})


# @app.callback(
#     Output("line-chart", "figure"))
# def update_line_chart():
#     fig = px.line(data, 
#         x="date", y="daily_profit")
#     return fig

app.run_server(debug=True)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')


