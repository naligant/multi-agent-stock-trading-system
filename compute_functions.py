import pandas as pd
import yfinance as yf
import numpy as np

def compute_rsi(stock_data, period=14):
    #day to day change in price
    delta = stock_data['Close'].diff()
    #gain is the average of the positive changes
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    #loss is the average of the negative changes
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    #relative strength index
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

#helper functions for computer_sma
def generate_signals(stock_data, short_window=20, long_window=20):
    stock_data = stock_data.copy()

    stock_data['SMA_short'] = stock_data['Adj Close'].rolling(window=short_window).mean()
    stock_data['SMA_long'] = stock_data['Adj Close'].rolling(window=long_window).mean()

    stock_data['signal'] = 0.0

    stock_data.loc[stock_data['SMA_short'] > stock_data['SMA_long'], 'signal'] = 1
    stock_data.loc[stock_data['SMA_short'] < stock_data['SMA_long'], 'signal'] = -1

    #convert signals into positions
    stock_data['position'] = stock_data['signal'].replace(to_replace=0, method='ffill').fillna(0)

    return stock_data

def compute_sma(stock_data, intial_cash=10000, commission=1.0):
    #generate trading signals
    stock_data = generate_signals(stock_data)

    #simulates profile if we followed the trading signals
    cash = intial_cash
    shares = 0
    last_pos = 0
    portfolio_values = []

    #loop through each day
    for idx, row in stock_data.iterrows():
        price = row['Adj Close']
        pos = row['position']
    
    #entering a long trade
    if last_pos <= 0 and pos == 1:
        shares = cash // price
        spent = shares * price + commission
        cash -= spent

    #exiting a long trade
    elif last_pos >= 0 and pos == -1:
        cash += shares * price - commission
        shares = 0

    #record portfolio value
    total = cash + shares * price
    portfolio_values.append({
        'date': idx,
        'total': total,
        'cash': cash,
        'shares': shares,
        'price': price,
        'pos': pos
    })

    last_pos = pos

    #return portfolio history
    pv = pd.DataFrame(portfolio_values).set_index('date')
    return pv
