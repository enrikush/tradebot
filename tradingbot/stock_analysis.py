import pandas as pd
from polygon import RESTClient
from datetime import date, timedelta
import talib as ta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import requests
import tkinter as tk
from grade import analyze_sentiment, grade_stock, scale_grade  # Assuming these are custom functions

client = RESTClient(api_key="fnjO7eJ68Yi1OQ9RWNdcJFNER0yFEHKO")
six_months_ago = date.today() - timedelta(days=6 * 30)

def calculate_moving_averages(df):
   if 'close' not in df.columns:
       raise ValueError("DataFrame does not have 'Close' column.")
   ema = ta.EMA(df['close'].values) 
   df['EMA'] = pd.Series(ema, index=df.index)
   return df

def calculate_rsi(df):
   
   rsi = ta.RSI(df['close'].values)
   df['RSI'] = pd.Series(rsi, index=df.index)
   return df

def calculate_bollinger_bands(df):
   if 'close' not in df.columns:
       raise ValueError("DataFrame does not have 'Close' column.")
   upper, middle, lower = ta.BBANDS(df['close'].values)
   df['Upper Band'] = pd.Series(upper, index=df.index)
   df['Middle Band'] = pd.Series(middle, index=df.index)
   df['Lower Band'] = pd.Series(lower, index=df.index)
   return df

def calculate_macd(df):
   if 'close' not in df.columns:
       raise ValueError("DataFrame does not have 'Close' column.")
   macd, signal, _ = ta.MACD(df['close'].values)
   df['MACD'] = pd.Series(macd, index=df.index)
   df['Signal Line'] = pd.Series(signal, index=df.index)
   return df

def calculate_ema(df, periods=[12, 26]):
   if 'close' not in df.columns:
       raise ValueError("DataFrame does not have 'Close' column.")
   for period in periods:
       ema = ta.EMA(df['close'].values, timeperiod=period)
       df[f'EMA_{period}'] = pd.Series(ema, index=df.index)
   return df

def calculate_obv(df):
   if 'close' not in df.columns or 'volume' not in df.columns:
       raise ValueError("DataFrame does not have 'Close' or 'Volume' column.")
   obv = ta.OBV(df['close'].values, df['volume'].values)
   df['OBV'] = pd.Series(obv, index=df.index)
   return df


def get_stock_data(symbol):
  
  aggs = []
  for a in client.list_aggs(ticker=symbol, multiplier=1, timespan="day", from_=six_months_ago, to=date.today(), limit=50000):
      aggs.append(a)

  # Convert aggregates into a DataFrame
  df = pd.DataFrame(aggs)
  print(df.head()) # Print the first few rows of the DataFrame
   

  return df


def fetch_and_analyze(symbol):
    try:
        aggs = []
        for a in client.list_aggs(ticker=symbol, multiplier=1, timespan="day", from_=six_months_ago, to=date.today(), limit=50000):
            aggs.append(a)

        # Convert aggregates into a DataFrame
        df = pd.DataFrame(aggs)

        # Calculate technical indicators
        df = calculate_moving_averages(df)
        df = calculate_rsi(df)
        df = calculate_bollinger_bands(df)
        df = calculate_macd(df)
        df = calculate_ema(df)
        df = calculate_obv(df)

        # Calculate sentiment
        news = get_news(symbol)
        if not news:
            return None

        avg_sentiment = analyze_sentiment(news)

        # Grade the stock
        grade = grade_stock(df, df['volume'].iloc[-1], avg_sentiment)

        # Prepare results as a dictionary
        results = {
            'stock_price': df['close'].iloc[-1],
            'volume': df['volume'].iloc[-1],
            'sentiment': avg_sentiment,
            'grade': grade,
            # ... other relevant information
        }

        return results
    except Exception as e:
        # Log the error for debugging
        print(f"Error in fetch_and_analyze: {str(e)}")
        return None





        

    
def plot_stock_data(df, symbol, root):
    fig = Figure(figsize=(14, 7), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(df.index, df['close'], label='close Price')
    
    # Plot additional technical indicators
    ax.plot(df.index, df['Upper Band'], label='Upper Band', linestyle='--')
    ax.plot(df.index, df['Middle Band'], label='Middle Band', linestyle='--')
    ax.plot(df.index, df['Lower Band'], label='Lower Band', linestyle='--')
    
    ax.plot(df.index, df['MACD'], label='MACD', linestyle='-.')
    ax.plot(df.index, df['Signal Line'], label='Signal Line', linestyle='-.')
    
    for period in [12, 26]:
        ax.plot(df.index, df[f'EMA_{period}'], label=f'EMA_{period}', linestyle=':')

    ax.set_title(f'Stock Data for {symbol}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price ($)')
    ax.legend(loc='upper left')

    

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

def get_news(symbol):
    api_key = "cb0163d7061944ff95a0305112b90057"
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "articles" in data:
            news = [
                {"date": article.get("publishedAt", ""), "title": article.get("title", ""),
                 "content": article.get("content", "")} for article in data["articles"]
            ]
            return news
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return []



    