from datetime import date
import datetime
import os
from jugaad_data.nse import stock_csv

STOCKS = ['COALINDIA', 'SBILIFE', 'SUNPHARMA', 'DRREDDY', 'HEROMOTOCO', 'CIPLA', 'BRITANNIA', 'BPCL', 'APOLLOHOSP', 'EICHERMOT', 'NTPC', 'SHREECEM', 'TATACONSUM', 'ADANIPORTS', 'ASIANPAINT', 'LT', 'BAJAJ-AUTO', 'BHARTIARTL', 'HINDUNILVR', 'NESTLEIND', 'INDUSINDBK', 'AXISBANK', 'WIPRO', 'MARUTI', 'UPL', 'M&M', 'TITAN', 'SBIN', 'ITC', 'ONGC', 'BAJAJFINSV', 'KOTAKBANK', 'TATAMOTORS', 'HDFCBANK', 'GRASIM', 'HDFCLIFE', 'TCS', 'ICICIBANK', 'HINDALCO', 'TECHM', 'RELIANCE', 'JSWSTEEL', 'BAJFINANCE', 'INFY', 'DIVISLAB', 'ULTRACEMCO', 'HCLTECH', 'TATASTEEL', 'POWERGRID', 'HDFCBANK']
DATES = (date(2023,1,1), datetime.datetime.now().date())

for stock in STOCKS:
    path = stock_csv(stock, DATES[0], DATES[1])
    os.rename(path, "data/"+ path)