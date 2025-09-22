import yfinance as yf
import numpy as np
import time
import os
import requests
import finnhub
from api_setup import market_data_agent, news_data_agent
from compute_functions import compute_sma, compute_rsi

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
if not FINNHUB_API_KEY:
    raise ValueError("FINNHUB_API_KEY is not set")

#market data agent
def get_stock_data(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        time.sleep(1)
        stock_data = stock.history(start=start_date, end=end_date)
        return stock_data
    except yf.exceptions.YFRateLimitError:
            print("Rate limit reached. Waiting 60 seconds before retrying...")
            time.sleep(60)  # Wait 60 seconds if we hit the rate limit
            return get_stock_data(ticker, start_date, end_date)

def get_news_data(ticker, news_dict):
    # url = f'https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2024-12-15&to=2024-12-31&token={FINNHUB_API_KEY}'
    finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
    news_data = finnhub_client.company_news(ticker, _from=start_date, to=end_date)
    news_dict['date'] = []
    news_dict['headline'] = []
    news_dict['summary'] = []
    for article in news_data:
            news_dict['date'].append(article['datetime'])
            news_dict['headline'].append(article['headline'])
            news_dict['summary'].append(article['summary'])



#test data
news_dict = {}
ticker = 'AAPL'
start_date = "2024-01-01"
end_date = "2025-01-01"

#enter in which stock you want to get data from
stock_data = get_stock_data(ticker, start_date, end_date)
# print(stock_data.tail())
print(stock_data)
ticker_, date, open, high, low, close, volume, dividends, stock_splits = market_data_agent(stock_data, ticker)
# print(date, open, high, low, close, volume, dividends, stock_splits)

#testing news data
get_news_data(ticker, news_dict)

# print(news_dict['headline'])
ans = news_data_agent(news_dict, ticker)
print(ans)

#testing rsi
rsi = compute_rsi(stock_data)
print(rsi)

