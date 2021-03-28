# %%
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
from pandas_datareader import data as pdr

# %matplotlib inline

my_year_month_fmt = mdates.DateFormatter('%m/%y')

tickers = ['CL=F', "NIO", "SPCE"]  # insert whichever tickers

start_date = '2019-06-01'
end_date = '2020-06-01'

data_table = pdr.DataReader(tickers, 'yahoo', start_date, end_date)

close = data_table['Close']
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
close = close.reindex(all_weekdays)
close = close.fillna(method='ffill')
data = close
data.tail(10)

short_rolling = data.rolling(window=5).mean()  # first moving average
long_rolling = data.rolling(window=50).mean()  # second moving average

ema_short = data.ewm(span=8, adjust=False).mean()

fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(data.loc[start_date:end_date, :].index,
        data.loc[start_date:end_date, 'CL=F'], label='Price of WTI Crude Oil')
ax.plot(ema_short.loc[start_date:end_date, :].index,
        ema_short.loc[start_date:end_date, 'CL=F'], label='5-days EMA')
ax.plot(short_rolling.loc[start_date:end_date, :].index,
        short_rolling.loc[start_date:end_date, 'CL=F'], label='8-days SMA')

ax.legend(loc='best')
ax.set_ylabel('Price in $')
ax.xaxis.set_major_formatter(my_year_month_fmt)

# calculate difference between price and EMA
trading_positions_raw = data - ema_short
trading_positions_raw.tail()

# buy signal by multipling by 1/3
trading_positions = trading_positions_raw.apply(np.sign) * 1/3
trading_positions.tail()

# lag
trading_positions_final = trading_positions.shift(1)


# entry / exit graph

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9))

ax1.plot(data.loc[start_date:end_date, :].index,
         data.loc[start_date:end_date, 'CL=F'], label='Price')
ax1.plot(ema_short.loc[start_date:end_date, :].index,
         ema_short.loc[start_date:end_date, 'CL=F'], label='Span 8-days EMA')

ax1.set_ylabel('$')
ax1.legend(loc='best')
ax1.xaxis.set_major_formatter(my_year_month_fmt)

ax2.plot(trading_positions_final.loc[start_date:end_date, :].index, trading_positions_final.loc[start_date:end_date, 'CL=F'],
         label='Trading position')

ax2.set_ylabel('Trading position')
ax2.xaxis.set_major_formatter(my_year_month_fmt)


# countinuously compoung return
asset_log_returns = np.log(data).diff()
asset_log_returns.head()
strategy_asset_log_returns = trading_positions_final * asset_log_returns
strategy_asset_log_returns.tail()

# cumulative return of stocks
# Get the cumulative log-returns per asset
cum_strategy_asset_log_returns = strategy_asset_log_returns.cumsum()

# Transform the cumulative log returns to relative returns
cum_strategy_asset_relative_returns = np.exp(
    cum_strategy_asset_log_returns) - 1

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9))

for c in asset_log_returns:
    ax1.plot(cum_strategy_asset_log_returns.index,
             cum_strategy_asset_log_returns[c], label=str(c))

ax1.set_ylabel('Cumulative log-returns')
ax1.legend(loc='best')
ax1.xaxis.set_major_formatter(my_year_month_fmt)

for c in asset_log_returns:
    ax2.plot(cum_strategy_asset_relative_returns.index, 100 *
             cum_strategy_asset_relative_returns[c], label=str(c))

ax2.set_ylabel('Total relative returns (%)')
ax2.legend(loc='best')
ax2.xaxis.set_major_formatter(my_year_month_fmt)

# strategy cumulative return
# Total strategy relative returns. This is the exact calculation.
cum_relative_return_exact = cum_strategy_asset_relative_returns.sum(axis=1)

# Get the cumulative log-returns per asset
cum_strategy_log_return = cum_strategy_asset_log_returns.sum(axis=1)

# Transform the cumulative log returns to relative returns. This is the approximation
cum_relative_return_approx = np.exp(cum_strategy_log_return) - 1

fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(cum_relative_return_exact.index, 100 *
        cum_relative_return_exact, label='Exact')
ax.plot(cum_relative_return_approx.index, 100 *
        cum_relative_return_approx, label='Approximation')

ax.set_ylabel('Total cumulative relative returns (%)')
ax.legend(loc='best')
ax.xaxis.set_major_formatter(my_year_month_fmt)

# asset return


def print_portfolio_yearly_statistics(portfolio_cumulative_relative_returns, days_per_year=52 * 5):

    total_days_in_simulation = portfolio_cumulative_relative_returns.shape[0]
    number_of_years = total_days_in_simulation / days_per_year

    # The last data point will give us the total portfolio return
    total_portfolio_return = portfolio_cumulative_relative_returns[-1]
    # Average portfolio return assuming compunding of returns
    average_yearly_return = (
        1 + total_portfolio_return)**(1/number_of_years) - 1

    print('Total portfolio return is: ' +
          '{:5.2f}'.format(100*total_portfolio_return) + '%')
    print('Average yearly return is: ' +
          '{:5.2f}'.format(100*average_yearly_return) + '%')


print_portfolio_yearly_statistics(cum_relative_return_exact)


# highlight difference between buy and hold and strategy
# Define the weights matrix for the simple buy-and-hold strategy
simple_weights_matrix = pd.DataFrame(
    1/3, index=data.index, columns=data.columns)

# Get the buy-and-hold strategy log returns per asset
simple_strategy_asset_log_returns = simple_weights_matrix * asset_log_returns

# Get the cumulative log-returns per asset
simple_cum_strategy_asset_log_returns = simple_strategy_asset_log_returns.cumsum()

# Transform the cumulative log returns to relative returns
simple_cum_strategy_asset_relative_returns = np.exp(
    simple_cum_strategy_asset_log_returns) - 1

# Total strategy relative returns. This is the exact calculation.
simple_cum_relative_return_exact = simple_cum_strategy_asset_relative_returns.sum(
    axis=1)

fig, ax = plt.subplots(figsize=(16, 9))

ax.plot(cum_relative_return_exact.index, 100 *
        cum_relative_return_exact, label='EMA strategy')
ax.plot(simple_cum_relative_return_exact.index, 100 *
        simple_cum_relative_return_exact, label='Buy and hold')

ax.set_ylabel('Total cumulative relative returns (%)')
ax.legend(loc='best')
ax.xaxis.set_major_formatter(my_year_month_fmt)

# return if buy and hold


def print_portfolio_yearly(portfolio_cumulative_relative_returns, days_per_year=52 * 5):

    total_days_in_simulation = portfolio_cumulative_relative_returns.shape[0]
    number_of_years = total_days_in_simulation / days_per_year

    # The last data point will give us the total portfolio return
    total_portfolio_return = portfolio_cumulative_relative_returns[-1]
    # Average portfolio return assuming compunding of returns
    average_yearly_return = (
        1 + total_portfolio_return)**(1/number_of_years) - 1

    print('Total portfolio return is: ' +
          '{:5.2f}'.format(100*total_portfolio_return) + '%')
    print('Average yearly return is: ' +
          '{:5.2f}'.format(100*average_yearly_return) + '%')


print_portfolio_yearly(simple_cum_relative_return_exact)
# %%
