from datetime import date
import datetime
import os
import shutil
from jugaad_data.nse import stock_csv

STOCKS = [
    "ADANIPORTS",  # Adani Ports and Special Economic Zone
    "APOLLOHOSP",
    "ASIANPAINT",  # Asian Paints
    "AXISBANK",    # Axis Bank
    "BAJAJ-AUTO",  # Bajaj Auto
    "BAJFINANCE",  # Bajaj Finance
    "BAJAJFINSV",  # Bajaj Finserv
    "BPCL",        # Bharat Petroleum Corporation
    "BHARTIARTL",  # Bharti Airtel
    "BRITANNIA",   # Britannia Industries
    "CIPLA",       # Cipla
    "COALINDIA",   # Coal India
    "DIVISLAB",    # Divi's Laboratories
    "DRREDDY",     # Dr. Reddy's Laboratories
    "EICHERMOT",   # Eicher Motors
    "GRASIM",      # Grasim Industries
    "HCLTECH",     # HCL Technologies
    "HDFCBANK",    # HDFC Bank
    "HDFCLIFE",    # HDFC Life Insurance Company
    "HEROMOTOCO",  # Hero MotoCorp
    "HINDALCO",    # Hindalco Industries
    "HINDUNILVR",  # Hindustan Unilever
    # "HDFC",        # Housing Development Finance Corporation
    "ICICIBANK",   # ICICI Bank
    "ITC",         # ITC Limited
    "IOC",         # Indian Oil Corporation
    "INDUSINDBK",  # IndusInd Bank
    "INFY",        # Infosys
    "JSWSTEEL",    # JSW Steel
    "KOTAKBANK",   # Kotak Mahindra Bank
    "LT",          # Larsen & Toubro
    "M&M",         # Mahindra & Mahindra
    "MARUTI",      # Maruti Suzuki
    "NTPC",        # NTPC
    "NESTLEIND",   # Nestlé India
    "ONGC",        # Oil and Natural Gas Corporation
    "POWERGRID",   # Power Grid Corporation of India
    "RELIANCE",    # Reliance Industries
    "SBILIFE",     # SBI Life Insurance
    "SHREECEM",    # Shree Cement
    "SBIN",        # State Bank of India
    "SUNPHARMA",   # Sun Pharmaceutical Industries
    "TCS",         # Tata Consultancy Services
    "TATACONSUM",  # Tata Consumer Products
    "TATAMOTORS",  # Tata Motors
    "TATASTEEL",   # Tata Steel
    "TECHM",       # Tech Mahindra
    "TITAN",       # Titan Company
    "UPL",         # UPL Limited
    "ULTRACEMCO",  # UltraTech Cement
    "WIPRO"        # Wipro
]

TODAY = datetime.datetime.now().date()
DATES = (TODAY - datetime.timedelta(days=365), TODAY- datetime.timedelta(days=0))

shutil.rmtree("data")
os.mkdir("data")
for stock in STOCKS:
    path = stock_csv(stock, DATES[0], DATES[1])
    os.rename(path, "data/"+ path)
