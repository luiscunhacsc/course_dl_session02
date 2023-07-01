import pandas as pd
import yfinance as yf
import pandas_ta as ta
from fredapi import Fred
from datetime import datetime

# Set your FRED API key
fred_api_key = "70445daf0b4c246acf5c9e93a7b76113"
fred = Fred(api_key=fred_api_key)

# Define date range
start_date = "1969-05-01"
end_date = "2023-03-21"

# Fetch S&P 500 data from Yahoo Finance
sp500 = yf.download('^GSPC', start=start_date, end=end_date)

# Fetch VIX and USDX data from Yahoo Finance
vix = yf.download('^VIX', start=start_date, end=end_date)
usdx = yf.download('DX-Y.NYB', start=start_date, end=end_date)

# Fetch EFFR, UNRATE, UMCSENT from FRED
effr = fred.get_series('DFF', start_date, end_date)
unrate = fred.get_series('UNRATE', start_date, end_date)
umcsent = fred.get_series('UMCSENT', start_date, end_date)

# Reindex DataFrames to match trading days
vix = vix.reindex(sp500.index)
usdx = usdx.reindex(sp500.index)
effr = effr.reindex(sp500.index)
unrate = unrate.reindex(sp500.index)
umcsent = umcsent.reindex(sp500.index)

# Fill missing UNRATE and UMCSENT values with the last known value
unrate = unrate.fillna(method='ffill')
umcsent = umcsent.fillna(method='ffill')

# Calculate MACD, RSI, and ATR technical indicators
macd = ta.macd(sp500['Close'])
rsi = ta.rsi(sp500['Close'])
atr = ta.atr(sp500['High'], sp500['Low'], sp500['Close'], length=14)

# Merge all data into a single DataFrame
data = pd.concat([
    sp500['Open'],
    sp500['Close'],
    macd['MACD_12_26_9'],
    rsi,
    atr,
    vix['Close'],
    usdx['Close'],
    effr,
    unrate,
    umcsent
], axis=1)

# Rename columns
data.columns = [
    'Open', 'Close', 'MACD', 'RSI', 'ATR', 'VIX', 'USDX', 'EFFR', 'UNRATE', 'UMCSENT'
]

# Save the updated data to CSV
data.to_csv('updated_sp500_data.csv')
