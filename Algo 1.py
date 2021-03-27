### IMPORTS ###
#%%
import pandas as pd
import yfinance as yf
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
from pandas_datareader import data as pdr

register_matplotlib_converters()
yf.pdr_override()  # Makes the Datareader use data from Yahoo Finance
### IMPORTS ###

ticker = yf.Ticker("CL=F")
print(ticker)
lastMonth = ticker.history(period="6mo")
print(lastMonth)
tickers = ['CL=F', "NIO", "SPCE"]

start_date = '2019-06-01'
end_date = '2020-06-01'

panel_data = pdr.DataReader(tickers, start_date, end_date)
print(panel_data)
# Retrieve the close prices
close = panel_data['Close']
# Create the axis with days
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
# Merge the close prices with axis.
close = close.reindex(all_weekdays)
close = close.fillna(method='ffill')
# Print the close prices table
print(close)
cl_f = close.loc[:, 'CL=F']

fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(cl_f.index, cl_f, label='WTI crude oil prices')

ax.set_xlabel('Date')

ax.set_ylabel('Adjusted closing price ($)')

ax.legend()
# YOUR CODE HERE
# Get the MSFT timeseries.
cl_f = close.loc[:, 'CL=F']
# Calculate the average for the last 20 days
short_rolling_cl_f = cl_f.rolling(window=20).mean()
# Create the plotting object.
fig, ax = plt.subplots(figsize=(16, 9))
# Plot the MSFT data.
ax.plot(cl_f.index, cl_f, label='CL=F')
#  Plot the last 20 days average.
ax.plot(short_rolling_cl_f.index, short_rolling_cl_f, label='20 days Average')
# Set the X Label
ax.set_xlabel('Date')
# Set the Y Label
ax.set_ylabel('Adjusted closing price ($)')
# Show legend
ax.legend()

# %%

# %%
