import pandas_datareader as pdr
import datetime 
import pandas as pd 
from datetime import date

nombres = pd.read_csv('Nombres.csv')
ahora = date.today()
dia = ahora.day - 1
mes = ahora.month
mesa = ahora.month - 1
mesb = (ahora.month - 7) % 12
año = ahora.year
añoa = ahora.year - 1
nombres = nombres.drop([65,78,95,119,158,325,338,445],axis=0)
nombres.reset_index(drop=True, inplace=True)
benchmark = pdr.get_data_yahoo('^GSPC',
                               start=datetime.datetime(añoa, mesb, dia),
                               end=datetime.datetime(año, mes, dia))
valori = (benchmark['Adj Close'][-1] - benchmark['Adj Close'][0])/benchmark['Adj Close'][0]
supero = pd.DataFrame(columns=['Empresa'],
                  index=range(len(nombres)))
nosupero = pd.DataFrame(columns=['Empresa'],
                  index=range(len(nombres)))
igual = pd.DataFrame(columns=['Empresa'],
                  index=range(len(nombres)))

for i in range(len(nombres)):
    aapl = pdr.get_data_yahoo(str(nombres['Symbol'][i]), 
                           start=datetime.datetime(año, mesa, dia), 
                           end=datetime.datetime(año, mes, dia))
    valor = (aapl['Adj Close'][-1] - aapl['Adj Close'][0])/aapl['Adj Close'][0]
    print(i)
    if valor > valori:
        supero["Empresa"][i] = str(nombres['Symbol'][i])
        
    elif valor < valori:
        nosupero["Empresa"][i] = str(nombres['Symbol'][i])
        
    else:
        igual["Empresa"][i] = str(nombres['Symbol'][i])
        
supero = supero.dropna()
supero.reset_index(drop=True, inplace=True)
nosupero = nosupero.dropna()
nosupero.reset_index(drop=True, inplace=True)
igual = igual.dropna()
igual.reset_index(drop=True, inplace=True)
        
print("Numero de empresas que superaron el benchmark:",len(supero))
print("Numero de empresas que no superaron el benchmark:",len(nosupero))
print("Numero de empresas que igualaron el benchmark:",len(igual))
        
                