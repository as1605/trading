from datetime import date
import json
import os
import requests

MF = ["Quant Small Cap Fund Direct Plan Growth","Motilal Oswal Midcap Fund Direct Growth","Quant Large Cap Fund Direct Growth","Groww Nifty EV & New Age Automotive ETF FoF Direct Growth","DSP The Infrastructure Growth and Economic Reforms Regular Fund Direct Growth","Nippon India Small Cap Fund Direct Growth","HDFC Mid Cap Opportunities Direct Plan Growth","Groww Value Fund Direct Growth","ICICI Prudential Innovation Fund Direct Growth","Aditya Birla Sun Life PSU Equity Fund Direct Growth","Quant Small Cap Fund Direct Plan Growth","ICICI Prudential Bluechip Fund Direct Growth","Motilal Oswal Midcap Fund Direct Growth","HDFC Balanced Advantage Fund Direct Plan Growth","Parag Parikh Flexi Cap Fund Direct Growth","Bandhan Small Cap Fund Direct Growth","Groww Nifty EV & New Age Automotive ETF FoF Direct Growth","Kotak Emerging Equity Fund Direct Growth","Quant Large Cap Fund Direct Growth","JM Flexicap Fund Direct Plan Growth","LIC MF Infrastructure Fund Direct Growth","Quant Small Cap Fund Direct Plan Growth","Motilal Oswal Midcap Fund Direct Growth","SBI Gold Direct Plan Growth","Motilal Oswal S&P 500 Index Fund Direct Growth","Bandhan Small Cap Fund Direct Growth","Nippon India Large Cap Fund Direct Growth","Edelweiss Mid Cap Direct Plan Growth","Quant Multi Asset Fund Direct Growth","Franklin India Smaller Companies Direct Fund Growth"]
TICKERS = ["M_QUNF","M_MOLS","M_QULP","M_GRNU","M_AXGG","M_NISL","M_HDCMS","M_INUI","M_ICPFV","M_ADTS","M_QUNF","M_ICCBH","M_MOLS","M_HDCBA","M_PARO","M_IDFM","M_GRNU","M_KORY","M_QULP","M_JMUU","M_IDIC","M_QUNF","M_MOLS","M_SBIGL","M_MOTA","M_IDFM","M_NIRL","M_EDME","M_QUNS","M_FRSM", "M_SBUP"]
TICKER_NAMES = {'M_QUNF': 'Quant Small Cap', 'M_MOLS': 'Motilal Oswal Midcap', 'M_QULP': 'Quant Large Cap', 'M_GRNU': 'Groww Nifty EV & New Age Automotive ETF FoF', 'M_AXGG': 'DSP The Infrastructure  and Economic Reforms Regular', 'M_NISL': 'Nippon India Small Cap', 'M_HDCMS': 'HDFC Mid Cap Opportunities', 'M_INUI': 'Groww Value', 'M_ICPFV': 'ICICI Prudential Innovation', 'M_ADTS': 'Aditya Birla Sun Life PSU Equity', 'M_ICCBH': 'ICICI Prudential Bluechip', 'M_HDCBA': 'HDFC Balanced Advantage', 'M_PARO': 'Parag Parikh Flexi Cap', 'M_IDFM': 'Bandhan Small Cap', 'M_KORY': 'Kotak Emerging Equity', 'M_JMUU': 'JM Flexicap', 'M_IDIC': 'LIC MF Infrastructure', 'M_SBIGL': 'SBI Gold', 'M_MOTA': 'Motilal Oswal S&P 500 Index', 'M_NIRL': 'Nippon India Large Cap', 'M_EDME': 'Edelweiss Mid Cap', 'M_QUNS': 'Quant Multi Asset', 'M_FRSM': 'Franklin India Smaller Companies', 'M_SBUP': 'SBI PSU'}
STOCKS = []
DAY_CHANGE = {}

def getTicker(mf):
    r = requests.get(f"https://api.tickertape.in/search?text={mf}&types=mutualfund&pageNumber=0", 
                     headers= {"accept-version": "8.14.0"}
    )
    parsed = r.json()
    try:
        id = parsed['data']['items'][0]['id']
    except:
        id = "NotFound"
    return id

def getPortfolio(ticker):
    day = date.today().day
    month = date.today().month
    year = date.today().year
    dir = f"data/mf/{day}-{month}-{year}"
    os.makedirs(dir, exist_ok=True)
    path = f"{dir}/{ticker}.json"

    r = requests.get(f"https://api.tickertape.in/mutualfunds/{ticker}/holdings")
    parsed = r.json()
    try:
        holdings = parsed['data']['currentAllocation']
        for holding in holdings:
            if holding['type'] == "Equity" and holding['sid'] and holding['sid'] not in STOCKS:
                STOCKS.append(holding['sid'])
    except:
        holdings = []
    with open(path, "w") as f:
        json.dump(holdings, f)
    
def getStocks():
    stocks = ",".join(STOCKS)
    r = requests.get(f"https://quotes-api.tickertape.in/quotes?sids={stocks}")
    for stock in r.json()['data']:
        # print(stock['sid'], stock['dyChange'])
        DAY_CHANGE[stock['sid']] = stock['dyChange']
    day = date.today().day
    month = date.today().month
    year = date.today().year
    dir = f"data/mf/{day}-{month}-{year}"
    path = f"{dir}/DAY_CHANGE.json"
    json.dump(DAY_CHANGE, open(path, "w"))

def getNAV(mf_ticker):
    day = date.today().day
    month = date.today().month
    year = date.today().year
    dir = f"data/mf/{day}-{month}-{year}"
    path = f"{dir}/{mf_ticker}.json"
    with open(path, "r") as f:
        holdings = json.load(f)
    nav = 0
    tot = 0
    for holding in holdings:
        try:
            nav += holding['latest']*DAY_CHANGE[holding['sid']]/100
            tot += holding['latest']
        except:
            pass
    return nav, tot


# for mf in MF:
#     TICKERS.append(getTicker(mf))

for ticker in TICKERS:
    getPortfolio(ticker)

getStocks()

changes = []
for ticker in TICKER_NAMES:
    nav, tot = getNAV(ticker)  
    changes.append((TICKER_NAMES[ticker], nav, tot))
changes.sort(key=lambda x: x[1], reverse=True)
for change in changes:
    if change[1] > 0:
        print("+", end="")
    print(f"{change[1]:.2f}\t{change[0]} ({change[2]:.2f}%)")

# M = []
# for mf in MF:
#     M.append(mf.replace("Direct", "").replace("Growth", "").replace("Plan", "").replace("Fund", "").strip())

# for (i, z) in zip(M, TICKERS):
#     TICKER_NAMES[z] = i
# print(TICKER_NAMES)