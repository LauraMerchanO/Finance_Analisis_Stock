import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from enum import Enum


class ActionColorMapping(Enum):
    SELL = 'red'
    BUY = 'green'


class ActionPricePoint:

    def __init__(self, price, date, action):
        self.price = price
        self.date = date
        self.action = action


def sell():
    return lambda left, right: left < right


def buy():
    return lambda left, right: left >= right


def plot(symbol,price, ma_20, ma_100, action_price_points):
    ax = price.plot()

    ma_20.plot(label='Moving Average 20 Days', ax=ax)
    ma_100.plot(label='Moving Average 100 Days', ax=ax)

    ax.set_xlabel('Date')
    ax.set_ylabel('Closing Price')
    ax.set_title( symbol +' Closing Price')
    ax.legend(loc='upper left')

    for position in action_price_points:
        plt.scatter(position.date, position.price, s=60, c=position.action.value)

    plt.show()


def retrieve_closing_price(symbol):
    df = pd.read_csv('{}.csv'.format(symbol))
    return df['Close']


def data_not_available(price):
    return np.isnan(price)


def calculate_moving_average_crossovers(symbol):
    closing_price = retrieve_closing_price(symbol)

    rm_20 = closing_price.rolling(window=20).mean()
    rm_100 = closing_price.rolling(window=100).mean()

    action = ActionColorMapping.SELL
    signal_detected = sell()
    signals = []

    for index in range(closing_price.size):
        if data_not_available(rm_20[index]) or data_not_available(rm_100[index]):
            continue

        if signal_detected(rm_20[index], rm_100[index]):
            mean_price = (rm_20[index] + rm_100[index]) / 2
            action = ActionPricePoint(mean_price, index, action)
            signals.append(action)

        if rm_20[index] >= rm_100[index]:
            action = ActionColorMapping.SELL
            signal_detected = sell()
        else:
            action = ActionColorMapping.BUY
            signal_detected = buy()

    plot(symbol,closing_price, rm_20, rm_100, signals)


if __name__ == '__main__':
    calculate_moving_average_crossovers('GOLD')
    
if __name__ == '__main__':
    calculate_moving_average_crossovers('CAT')
    
if __name__ == '__main__':
    calculate_moving_average_crossovers('BTC-USD')
    
