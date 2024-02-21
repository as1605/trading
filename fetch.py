from datetime import date
import datetime
import os
import shutil
from jugaad_data.nse import stock_csv

STOCKS = ['COALINDIA', 'SBILIFE', 'SUNPHARMA', 'DRREDDY', 'HEROMOTOCO', 'CIPLA', 'BRITANNIA', 'BPCL', 'APOLLOHOSP', 'EICHERMOT', 'NTPC', 'SHREECEM', 'TATACONSUM', 'ADANIPORTS', 'ASIANPAINT', 'LT', 'BAJAJ-AUTO', 'BHARTIARTL', 'HINDUNILVR', 'NESTLEIND', 'INDUSINDBK', 'AXISBANK', 'WIPRO', 'MARUTI', 'UPL', 'M&M', 'TITAN', 'SBIN', 'ITC', 'ONGC', 'BAJAJFINSV', 'KOTAKBANK', 'TATAMOTORS', 'HDFCBANK', 'GRASIM', 'HDFCLIFE', 'TCS', 'ICICIBANK', 'HINDALCO', 'TECHM', 'RELIANCE', 'JSWSTEEL', 'BAJFINANCE', 'INFY', 'DIVISLAB', 'ULTRACEMCO', 'HCLTECH', 'TATASTEEL', 'POWERGRID', 'HDFCBANK']
TODAY = datetime.datetime.now().date()
DATES = (TODAY - datetime.timedelta(days=365), TODAY)

shutil.rmtree("data")
os.mkdir("data")
for stock in STOCKS:
    path = stock_csv(stock, DATES[0], DATES[1])
    os.rename(path, "data/"+ path)