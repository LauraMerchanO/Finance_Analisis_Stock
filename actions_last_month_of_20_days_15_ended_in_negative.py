import pandas_datareader as pdr
import datetime 
import pandas as pd 
from datetime import date

nasdaq = pd.read_csv('tickers-nasdaq-100.csv')
ahora = date.today()
dia = ahora.day - 1
mes = ahora.month
mesa = ahora.month - 1
año = ahora.year

Total = pd.DataFrame(columns=['Empresa','Negativo'],
                  index=range(len(nasdaq)))
for i in range(len(nasdaq)):
    aapl = pdr.get_data_yahoo(str(nasdaq['Ticker'][i]), 
                           start=datetime.datetime(año, mesa, dia), 
                           end=datetime.datetime(año, mes, dia))
    h = 0
    for j in range(len(aapl)):
        if j != len(aapl)-1:
            if aapl["Adj Close"][j+1] - aapl["Adj Close"][j] < 0:
                h = h+1        
                
    if h >= 15:
        Total["Empresa"][i] = str(nasdaq['Ticker'][i])
        Total["Negativo"][i] = h

Total = Total.dropna()
Total.reset_index(drop=True, inplace=True)
print("Numero de empresas que quedaron en negativo en 15 dias:",len(Total))
