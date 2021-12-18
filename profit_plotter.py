import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
# import dash_bootstrap_components as dbc
from utility import striped_date_format
import time
# Fetch data
from portfolio import Portfolio
from stock_service import StockService

FETCHING_UPDATED_ORDER_LIST = False

def create_portfolio(name):
    # create portfolio
    portfolio = Portfolio(portfolio_name='my_investment_portfolio')
    # load the data
    portfolio.load()
    # create data
    daily_profit_data = StockService.calculate_profit_loss_df(portfolio.order_list)
    # plot the data
    print(daily_profit_data.shape)
    return daily_profit_data, portfolio

def filter_fetched_data(data):
    # required data
    required_cols = ['date']
    profit_col = [col for col in data.columns if '_profit' in col]
    required_cols.extend(profit_col)

    data = data[required_cols]
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
    return data, stock_checklist_dict, stock_checklist_values


data, portfolio = create_portfolio('my_investment_portfolio')
data, stock_checklist_dict, stock_checklist_values = filter_fetched_data(data)

#crete a dropdown orderlist checklist
order_list = portfolio.order_list
order_list_checklist = [{'label': str(order.order_date) + '    |    '+ str(order.symbol) + '    |    '+ str(order.quantity), 'value': str(order.order_id)} for order in order_list]
order_list_value = [each_oder['value'] for each_oder in order_list_checklist]


# graph 
fig = px.line(data, x="date", y=data.columns[1:])
fig.update_traces(mode="markers+lines", hovertemplate=None)
fig.update_layout(hovermode="x")

# App for plotting
app = dash.Dash(__name__, #external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


app.layout = html.Div([
    # stock check list
    dcc.Dropdown(
        options=stock_checklist_dict,
                value=stock_checklist_values,
                multi=True,
                 id='stock_checklist'),
    # # graph
    html.Br(),
    html.Br(),
    dcc.Graph(figure=fig, id='portfolio-profit-graph'),
    # Header
    html.Summary('Order list, Select and unselect to see the profit/loss based on only selected orders...', 
    style={'text-align': 'center', 'font-size': '15px', 'font-weight': 'bold', 'color': '#0066ff'}),
    html.Br(),
    #  order checklist
     dcc.Loading(
            id="loading-1", type="default", children=html.Div(id="loading-output-1")
        ),
    dcc.Dropdown(
        options=order_list_checklist,
                value=order_list_value,
                multi=True,
             id='order_checklist'),
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


@app.callback(Output("stock_checklist", "value"), Input("order_checklist", "value"))
def update_orders(checked_orders):
    #filter the data
    global data
    global FETCHING_UPDATED_ORDER_LIST
    FETCHING_UPDATED_ORDER_LIST = True
    selected_order_objs = [obj for obj in portfolio.order_list if str(obj.order_id) in checked_orders]
    data = StockService.calculate_profit_loss_df(selected_order_objs)
    data, stock_checklist_dict, stock_checklist_values  = filter_fetched_data(data)
    FETCHING_UPDATED_ORDER_LIST = False
    return stock_checklist_values

@app.callback(
    Output("loading-output-1", "children"),
    Input("order_checklist", "value"),
    prevent_initial_call=True,
)
def input_triggers_spinner(value):
    while True:
        if FETCHING_UPDATED_ORDER_LIST:
            time.sleep(5)
        else:
            break
    return "UPDATED"


# https://community.plotly.com/t/code-in-if---name-----main---runs-twice/5868
# https://community.plotly.com/t/dash-multi-page-app-functions-are-called-twice-unintentionally/46450
# adding use_reloader to stop calling function twice
app.run_server(debug=True, use_reloader = False)

if __name__ == '__main__':
    app.run_server(host='0.0.0.0')


