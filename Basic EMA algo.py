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

%matplotlib inline

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


# %%
