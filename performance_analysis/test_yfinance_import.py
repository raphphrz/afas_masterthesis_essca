# test_yfinance_import.py

import yfinance as yf

ticker = "AAPL"
data = yf.download("ACEIX", start="2022-01-01", end="2022-12-31", auto_adjust=True)


print(data.head())