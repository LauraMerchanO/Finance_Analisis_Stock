from pandas_datareader import data as pdr
import pandas as pd
from datetime import date

import numpy as np
from yahoofinancials import YahooFinancials

def maximos(diccionario, n):
    maximos_n = {}
    minimos_n = {}
    minimos_n.update(diccionario)
    while len(maximos_n) != n:
        maximos_n[max(minimos_n.items(), key=lambda x: x[1])[0]]= max(minimos_n.values())
        del minimos_n[max(minimos_n.items(), key=lambda x: x[1])[0]]
    return maximos_n

def minimos(diccionario, n):
    min_n = {}
    max_n = {}
    max_n.update(diccionario)
    while len(min_n) != n:
        min_n[min(max_n.items(), key=lambda x: x[1])[0]]= min(max_n.values())
        del max_n[min(max_n.items(), key=lambda x: x[1])[0]]
    return min_n
        

df = pd.read_excel('tickers nasdaq 100.xlsx', sheet_name='Hoja1')

elems = list(set(df['Ticker']))
end_time = date(2020, 4, 5)
start_time = date(2020, 3, 5)


def sharpe(ticker, start_time, end_time):
    all_data = pdr.get_data_yahoo(ticker,  start_time, end_time)
    short_window = 40
    long_window = 100
    signals = pd.DataFrame(index=all_data.index)
    signals['signal'] = 0.0
    signals['short_mavg'] = all_data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = all_data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] 
                                                > signals['long_mavg'][short_window:], 1.0, 0.0)   
    signals['positions'] = signals['signal'].diff()
    initial_capital= float(100000.0)
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    positions[ticker] = 100*signals['signal']   
    portfolio = positions.multiply(all_data['Adj Close'], axis=0)
    pos_diff = positions.diff()
    portfolio['holdings'] = (positions.multiply(all_data['Adj Close'], axis=0)).sum(axis=1)
    portfolio['cash'] = initial_capital - (pos_diff.multiply(all_data['Adj Close'], axis=0)).sum(axis=1).cumsum()   
    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change()
    returns = portfolio['returns']
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std())
    return sharpe_ratio
val={}
for i in elems:
    val[i] = sharpe(i,date(2020, 3, 5),date(2021, 3, 5))


volatibilidad = {}
for i in elems:
    stock_symbol = i
    end = end_time.strftime('%Y-%m-%d')
    start = start_time.strftime('%Y-%m-%d')
    json_prices = YahooFinancials(stock_symbol).get_historical_price_data(start, end, 'daily')
    prices = pd.DataFrame(json_prices[stock_symbol]['prices'])[['formatted_date', 'close']]
    prices.sort_index(ascending=False, inplace=True)
    prices['returns'] = (np.log(prices.close /prices.close.shift(-1)))
    daily_std = np.std(prices.returns)
    std = daily_std * 252 ** 0.5
    volatibilidad[stock_symbol] = str(np.round(std*100, 1))
sortVal = maximos(val,50)
sortVol = minimos(volatibilidad,50)

MORE_VALUE_LEESS_RISK = []
for i in sortVal:
    if i in sortVol:
        MORE_VALUE_LEESS_RISK.append(i)
print(MORE_VALUE_LEESS_RISK)
        
            
            
