# portfolio_profit_tracker

A simple tool to display the daily profit for the list of stocks.

step 1: Run the following command.

    python -m venv venv
    pip install -r requirements.txt

step 2: Download the data from zerodha. Go to orders and fetch history. Download the data as csv and save in data/reports.
else, create a csv ,sample file is in data/sample_data.

step 3: run:

    python profit_plotter.py

## CheckList

    [x] Fetch stock data
    [x] Store stocks data
    [ ] Dataset to plot
    [ ] Handle sell orders
    [ ] Plot profit
    [ ] Add logger
    [ ] Add series other than EQ, like A,B ...
    [ ] Predit profit for each stock in portfolio
    [ ] load data from custom file format
    [ ] UI to load file
