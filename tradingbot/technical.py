
import pandas as pd
from polygon import RESTClient
from datetime import date, timedelta
from textblob import TextBlob
import talib as ta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import requests
import tkinter as tk
client = RESTClient(api_key="fnjO7eJ68Yi1OQ9RWNdcJFNER0yFEHKO")
six_months_ago = date.today() - timedelta(days=6*30)

def get_stock_data(symbol):
  
  aggs = []
  for a in client.list_aggs(ticker=symbol, multiplier=1, timespan="day", from_=six_months_ago, to=date.today(), limit=50000):
      aggs.append(a)

  # Convert aggregates into a DataFrame
  df = pd.DataFrame(aggs)
  print(df.head()) # Print the first few rows of the DataFrame
   

  return df

def technicalAnalysis(get_stock_data, symbol):
   df = get_stock_data(symbol)




   # Ensure necessary columns exist
   if not set(['Close', 'High', 'Low', 'Open', 'Volume']).issubset(df.columns):
       raise ValueError("Missing necessary columns in dataframe")

   # Overlap Studies
   df['BBANDS_Upper'], df['BBANDS_Middle'], df['BBANDS_Lower'] = ta.BBANDS(df['Close'])
   df['DEMA'] = ta.DEMA(df['Close'])
   df['EMA'] = ta.EMA(df['Close'])
   df['HT_TRENDLINE'] = ta.HT_TRENDLINE(df['Close'])
   df['KAMA'] = ta.KAMA(df['Close'])
   df['MA'] = ta.MA(df['Close'])
   df['MAMA'] = ta.MAMA(df['Close'])
   df['MAVP'] = ta.MAVP(df['Close'])
   df['MIDPOINT'] = ta.MIDPOINT(df['Close'])
   df['MIDPRICE'] = ta.MIDPRICE(df['High'], df['Low'])
   df['SAR'] = ta.SAR(df['High'], df['Low'])
   df['SAREXT'] = ta.SAREXT(df['High'], df['Low'])
   df['SMA'] = ta.SMA(df['Close'])
   df['T3'] = ta.T3(df['Close'])
   df['TEMA'] = ta.TEMA(df['Close'])
   df['TRIMA'] = ta.TRIMA(df['Close'])
   df['WMA'] = ta.WMA(df['Close'])

   # Momentum Indicators
   df['ADX'] = ta.ADX(df['High'], df['Low'], df['Close'])
   df['ADXR'] = ta.ADXR(df['High'], df['Low'], df['Close'])
   df['APO'] = ta.APO(df['Close'])
   df['AROON'] = ta.AROON(df['High'], df['Low'])
   df['AROONOSC'] = ta.AROONOSC(df['High'], df['Low'])
   df['BOP'] = ta.BOP(df['Open'], df['High'], df['Low'], df['Close'])
   df['CCI'] = ta.CCI(df['High'], df['Low'], df['Close'])
   df['CMO'] = ta.CMO(df['Close'])
   df['DX'] = ta.DX(df['High'], df['Low'], df['Close'])
   df['MACD'], df['MACDsignal'], df['MACDhist'] = ta.MACD(df['Close'])
   df['MACDEXT'], df['MACDsignalEXT'], df['MACDhistEXT'] = ta.MACDEXT(df['Close'])
   df['MACDFIX'], df['MACDsignalFIX'], df['MACDhistFIX'] = ta.MACDFIX(df['Close'])
   df['MFI'] = ta.MFI(df['High'], df['Low'], df['Close'], df['Volume'])
   df['MINUS_DI'] = ta.MINUS_DI(df['High'], df['Low'], df['Close'])
   df['MINUS_DM'] = ta.MINUS_DM(df['High'], df['Low'])
   df['MOM'] = ta.MOM(df['Close'])
   df['PLUS_DI'] = ta.PLUS_DI(df['High'], df['Low'], df['Close'])
   df['PLUS_DM'] = ta.PLUS_DM(df['High'], df['Low'])
   df['PPO'] = ta.PPO(df['Close'])
   df['ROC'] = ta.ROC(df['Close'])
   df['ROCP'] = ta.ROCP(df['Close'])
   df['ROCR'] = ta.ROCR(df['Close'])
   df['ROCR100'] = ta.ROCR100(df['Close'])
   df['RSI'] = ta.RSI(df['Close'])
   df['STOCH'] = ta.STOCH(df['High'], df['Low'], df['Close'])
   df['STOCHF'] = ta.STOCHF(df['High'], df['Low'], df['Close'])
   df['STOCHRSI'] = ta.STOCHRSI(df['Close'])
   df['TRIX'] = ta.TRIX(df['Close'])
   df['ULTOSC'] = ta.ULTOSC(df['High'], df['Low'], df['Close'])
   df['WILLR'] = ta.WILLR(df['High'], df['Low'], df['Close'])

   return df
