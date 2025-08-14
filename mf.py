from datetime import date
import json
import os
import requests

TICKER_NAMES = {
    "M_IDFM": "Bandhan Small Cap",
    "M_DSPID": "DSP TIGER",
    "M_EDME": "Edelweiss Mid Cap",
    "M_FRSM": "Franklin Small Cap",
    "M_HDCBA": "HDFC Balanced",
    "M_HDCEQ": "HDFC Flexi",
    "M_HDCMS": "HDFC Mid Cap",
    "M_ICPFV": "ICICI Innovation",
    "M_ICPPP": "ICICI Multi Asset",
    "M_INOQ": "Invesco Global",
    "M_KORY": "Kotak Mid Cap",
    "M_LIIM": "LIC Infra",
    "M_MOLS": "Motilal Mid Cap",
    "M_NIPU": "Nippon Multi Asset",
    "M_NIML": "Nippon Multi Cap",
    "M_NIMS": "Nippon Small Cap",
    "M_PARO": "Parag Flexi",
    "M_QUNS": "Quant Multi Asset",
    "M_QUNF": "Quant Small Cap",
    "M_SBICO": "SBI Contra",
    "M_SBIGL": "SBI Gold",
    "M_SBTO": "SBI Multi Asset",
    "M_SBIVR": "SBI Silver",
    "M_TASC": "Tata Small Cap",
    "M_WOMT": "WhiteOak Multi Asset"
}
STOCKS = []
DAY_CHANGE = {}


def getTicker(mf):
    r = requests.get(
        f"https://api.tickertape.in/search?text={mf}&types=mutualfund&pageNumber=0",
        headers={"accept-version": "8.14.0"},
    )
    parsed = r.json()
    try:
        id = parsed["data"]["items"][0]["id"]
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
        holdings = parsed["data"]["currentAllocation"]
        for holding in holdings:
            if (
                holding["type"] == "Equity"
                and holding["sid"]
                and holding["sid"] not in STOCKS
            ):
                STOCKS.append(holding["sid"])
    except:
        holdings = []
    with open(path, "w") as f:
        json.dump(holdings, f)


def getStocks():
    stocks = ",".join(STOCKS)
    r = requests.get(f"https://quotes-api.tickertape.in/quotes?sids={stocks}")
    for stock in r.json()["data"]:
        # print(stock['sid'], stock['dyChange'])
        DAY_CHANGE[stock["sid"]] = stock["dyChange"]
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
            nav += holding["latest"] * DAY_CHANGE[holding["sid"]] / 100
            tot += holding["latest"]
        except:
            pass
    return nav, tot


if __name__ == "__main__":
    for ticker in TICKER_NAMES:
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
