import requests
import datetime
from indices.symbols import NIFTY50

HOME = "https://www.nseindia.com"
BASE_URL = "https://www.nseindia.com/api/option-chain-equities?symbol="
PRICE_URL = "https://www.nseindia.com/api/quote-equity?symbol="


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36" ,
    "referer": HOME
}
session = requests.Session()
session.get(HOME, headers=headers)


def get_weighted_average(symbol):
    url = BASE_URL + symbol
    
    r = session.get(url, headers=headers)
    data = r.json()["filtered"]["data"]
    datestring = r.json()["records"]["expiryDates"][0]
    #  %d-%b-%Y
    date = datetime.datetime.strptime(datestring, "%d-%b-%Y")
    date = datetime.date(date.year, date.month, date.day)
    today = datetime.date.today()
    daystillexpiry = (date-today).days
    
    
    weight = 0
    estimate = 0
    for d in data:
        if "CE" in d:
            wc = d["CE"]["lastPrice"]*d["CE"]["openInterest"]
            ec= d["strikePrice"] + d["CE"]["lastPrice"]
        else :
            wc=0
            ec=0
        if "PE" in d:
            wp = d["PE"]["lastPrice"]*d["PE"]["openInterest"]
            ep= d["strikePrice"] - d["PE"]["lastPrice"]
        else :
            wp=0
            ep=0
        
        

        weight += wc + wp
        estimate += ep*wp + ec*wc

    return estimate/weight , daystillexpiry


def get_price(symbol):
    url = PRICE_URL + symbol
    r = session.get(url, headers=headers)
    return r.json()["priceInfo"]["lastPrice"]


SYMBOLS= NIFTY50
for symbol in SYMBOLS:
    try:
        
        price= get_price(symbol)
        average,days = get_weighted_average(symbol)
        if price<average:
            print("\033[32m",end="")
            print(f"Buy  {symbol:^11} at {price:8.2f} and sell at {average:8.2f} and profit {(average-price)*100/average:5.2f}% in {days:2} days")
            print("\033[0m",end="")
        else:  
            print("\033[31m",end="")
            print(f"Sell {symbol:^11} at {price:8.2f} and buy  at {average:8.2f} and profit {(price-average)*100/average:5.2f}% in {days:2} days")
            print("\033[0m",end="")

       
        
    except:
        print(f"Error in fetching data for {symbol}")
        pass

