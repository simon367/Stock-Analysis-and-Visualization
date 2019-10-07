import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
style.use('ggplot')

# Read in CSV

df = pd.read_csv('big_five_stocks.csv')
df.head()

# Rename and Set Index to Proper Datetime Format
df.rename(columns={'Unnamed: 0': 'date'}, inplace = True)
df.set_index('date', inplace=True)
df.index = pd.to_datetime(df.index)

# Create List and Dictionary of Stock Names/Values
stock_names = df['name'].unique().tolist()
df_dict = {}
for stock in stock_names:
    df_dict[stock] = df[(df['name'] == stock)]

# Plot All Stocks On One Graph
ax1 = plt.subplot2grid((8,1), (0,0), rowspan=10, colspan=3)
for stock in stock_names:
    ax1.plot(df_dict[stock].index, df_dict[stock]['close'])
    ax1.legend(stock_names)

# Candlestick Graph of AAPL With Stock Volume Just Below
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
df_AAPL = df[df['name'] == 'AAPL']
df_AAPL1 = df_AAPL.loc['2000-01-01':]
df_ohlc = df_AAPL1['close'].resample('1M').ohlc()
df_volume = df_AAPL1['volume'].resample('1M').sum()

df_ohlc = df_ohlc.reset_index()
df_ohlc['date'] = df_ohlc['date'].map(mdates.date2num)
fig = plt.figure(figsize=(18, 16))
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
ax1.xaxis_date()
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num),df_volume.values,0)

# Pivot Dataframe and Show Correlation Table
df_close = df.pivot(columns='name', values='close')
df1 = df_close.dropna()
df1.corr()

# Standard Deviation and Low Point for Each Stock
for stock in stock_names:
    print (stock + ' standard deviation is : ' + str(df1[stock].std()))
for stock in stock_names:
    print (stock + ' low point is ' + str(df1[stock].min()) + ' which occured on ' + str(df1[stock].idxmin()))

# Visualization of Correlation Table
f = plt.figure(figsize=(10, 10))
plt.matshow(df_close.corr(), fignum=f.number)
plt.xticks(range(df_close.shape[1]), df_close.columns, fontsize=14)
plt.yticks(range(df_close.shape[1]), df_close.columns, fontsize=14)
cb = plt.colorbar()
cb.ax.tick_params()
plt.show()
