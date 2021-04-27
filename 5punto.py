import pandas as pd 
import yfinance as yf

df_list = pd.read_html('https://finance.yahoo.com/world-indices/')
majorStockIdx = df_list[0]
majorStockIdx.head()
tickerData = yf.Ticker('^GSPC')
tickerDf1 = tickerData.history(period='1d', start='2021-3-8', end='2021-3-8')
stock_list = []
for s in majorStockIdx.Symbol:
    tickerData = yf.Ticker(s)
    tickerDf1 = tickerData.history(period='1d', start='2021-3-8', end='2021-3-9')
    tickerDf1['ticker'] = s
    stock_list.append(tickerDf1)
msi = pd.concat(stock_list, axis = 0)
mean_df = msi['Close'].mean()
df = msi[(msi.Close > mean_df)]
lista = df['ticker']
superaron = list(lista)


