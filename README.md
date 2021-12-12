# portfolio_profit_tracker

A simple tool to display the daily profit for the list of stocks.

step 1: Run the following command.

    python -m venv venv
    pip install -r requirements.txt

step 2: Download the data from zerodha. Go to orders and fetch history. Download the data as csv and save in data/reports.
else, create a csv ,sample file is in data/sample_data.

    PLEASE ADD IPO ORDER MANUALLY!!!
    To check the IPO order details. Fo to holdings in zerodha, click ... option button (available with sotck name), Click on "View Breakdown".You will get id, date purched about , quantity details.

step 3: run:

    python profit_plotter.py

## CheckList

    [x] Fetch stock data
    [x] Store stocks data
    [x] Dataset to plot
    [ ] Handle sell orders
    [x] Plot profit
    [ ] Add logger
    [ ] Add series other than EQ, like A,B ...
    [ ] Predit profit for each stock in portfolio
    [ ] load data from custom file format
    [ ] UI to load file
    [ ] Add custom custom stocks (IPO sotcks will be not in order list)
