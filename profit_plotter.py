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
# required data
required_cols = ['date']
profit_col = [col for col in data.columns if '_profit' in col]
required_cols.extend(profit_col)

data = data[required_cols]

# graph 
fig = px.line(data, x="date", y=data.columns[1:])
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x")

# create data for app
# todo: store stoke in a seperate place
stock_checklist_dict = []
stock_checklist_values = []
stock_cols = profit_col
for element in ['daily_profit_and_loss', 'day_profit_status']:
    if element in stock_cols:
        stock_cols.remove(element)

for each_stock in stock_cols:
    each_stock_name = each_stock.split('_')[0]
    stock_checklist_dict.append({'label': each_stock_name, 'value': each_stock_name})
    stock_checklist_values.append(each_stock_name)

# App for plotting
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

app.layout = html.Div([
    #stock check list
    dcc.Checklist(
        options=stock_checklist_dict,
                value=stock_checklist_values,
                labelStyle={'display': 'inline-block'}
            , id='stock_checklist'),
    # graph
     dcc.Graph(figure=fig, id='portfolio-profit-graph'),
], id='main-div', style = {'display': 'inline-block','height' : '95%', 'width': '95%'})


@app.callback(Output("portfolio-profit-graph", "figure"), Input("stock_checklist", "value"))
def update_line_chart(stocks_selected):
    #filter the data
    req_col = ['date', 'daily_profit_and_loss', 'day_profit_status']
    for each_stock in stocks_selected:
        each_stock = each_stock + '_profit'
        req_col.append(each_stock)
    updated_data  = data[req_col]
    fig = fig = px.line(updated_data, x="date", y=updated_data.columns[1:])
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x")
    return fig

app.run_server(debug=True)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')


