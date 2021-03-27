# Retrieve, diplay and graph financial data


# %%
import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
from pandas_datareader import data as pdr

register_matplotlib_converters()
yf.pdr_override()  # Makes the Datareader use data from Yahoo Finance


# 1) retrieve and read stock information
stock = yf.Ticker("CL=F")
print(stock)
lastMonth = stock.history(period="6mo")
print(lastMonth)

# 2) Display stock price on pannel
tickers = ['CL=F', "NIO", "SPCE"]  # insert whichever tickers

start_date = '2019-06-01'
end_date = '2020-06-01'

data_table = pdr.DataReader(tickers, start_date, end_date)
print(data_table)

close = data_table['Close']  # data to look for
# Create the axis with days
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
# Merge the close prices with axis.
close = close.reindex(all_weekdays)
close = close.fillna(method='ffill')
# Print the close prices table
print(close)

# 3) Display stock prices on graph

graph_data = close.loc[:, 'CL=F']  # whichever stock

fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(graph_data.index, graph_data,
        label='WTI crude oil prices')  # label stock name

ax.set_xlabel('Date')

ax.set_ylabel('Adjusted closing price ($)')

ax.legend()

# 4) Building average trend line

stock_average = close.loc[:, 'CL=F']  # whichever stock
# Calculate average
short_rolling_stock_average = stock_average.rolling(
    window=20).mean()  # average mean
# Plotting
fig, ax = plt.subplots(figsize=(16, 9))
# Plot the MSFT data.
ax.plot(stock_average.index, stock_average, label='CL=F')
#  Plot the last 20 days average.
ax.plot(short_rolling_stock_average.index,
        short_rolling_stock_average, label='20 days Average')

ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()

# %%
