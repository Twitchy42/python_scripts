from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime

#We can adjust the tickers and years as we want
tickers = ['MSFT', 'HAS', 'AAPL', 'TMUS', 'YHOO']
years = 6

data_source = 'google'

end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=years*365)

#the matplotlib figure was throwing errors for the start date not being rounded
start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

#Gets the historical data from google finance
panel_data = data.DataReader(tickers, data_source, start_date, end_date)

#get just the closing price for each. finding this get_loc value was trial and error
adj_close = panel_data.loc._get_loc(3,0)

#disregard weekends
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
adj_close = adj_close.reindex(all_weekdays)

adj_close = adj_close.fillna(method="ffill")

#separate out each stock's data
stocks = []
for s in tickers:
    stocks.append(adj_close.ix[:, s])

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

#plot a line for each stock
for i in stocks:
    ax.plot(i.index, i, label = i.name)

ax.set_xlabel('Date')
ax.set_ylabel('Closing price ($)')
ax.legend()

plt.savefig("stocks.png")
