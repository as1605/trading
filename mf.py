from datetime import date
import json
import math
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
    "M_WOMT": "WhiteOak Multi Asset",
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


def get_returns(mf_ticker: str, duration: str) -> float:
    r = requests.get(
        f"https://api.tickertape.in/mutualfunds/{mf_ticker}/charts/inter?duration={duration}"
    )
    if r.status_code == 200:
        data = r.json()
        return data["data"][0]["r"]
    return 0

def get_sip(mf_ticker: str, duration: str) -> float:
    r = requests.get(
        f"https://api.tickertape.in/mutualfunds/{mf_ticker}/charts/inter?duration={duration}"
    )
    if r.status_code == 200:
        data = r.json()
        points = data["data"][0]["points"]

        invested = 0
        units = 0
        mo = "-".join(points[0]["ts"].split("-")[:2])
        for point in points:
            cu = "-".join(point["ts"].split("-")[:2])
            if cu != mo:
                invested += 1
                units += 1/point["lp"]
        price = units * points[-1]["lp"]
        return 100*(price/invested - 1)
    return 0

if __name__ == "__main__":
    for ticker in TICKER_NAMES:
        getPortfolio(ticker)

    getStocks()

    changes = []
    change_dict = {}
    for ticker in TICKER_NAMES:
        nav, tot = getNAV(ticker)
        change_dict[TICKER_NAMES[ticker]] = nav
        changes.append((TICKER_NAMES[ticker], nav, tot))
    changes.sort(key=lambda x: x[1], reverse=True)

    for change in changes:
        if change[1] > 0:
            print("+", end="")
        print(f"{change[1]:.2f}\t{change[0]:20} ({change[2]:.2f}%)")

    returns = []
    total_s = 0
    for ticker in TICKER_NAMES:
        change = change_dict[TICKER_NAMES[ticker]]
        r3y = get_returns(ticker, "3y") + change
        r1m = get_returns(ticker, "1mo") + change
        sip = get_sip(ticker, "3y") + change
        xirr = 100*(math.pow(1+(sip/100), 1/3) - 1)
 #       print(ticker, sip, xirr)
        s = r1m * xirr
        total_s += s
        returns.append((TICKER_NAMES[ticker], sip, r1m, s, xirr))

    returns.sort(key=lambda x: x[3])
    for return_data in returns:
        print(
                f"{return_data[0]:20}:\t 3Y SIP: {return_data[1]:.2f}%,\t XIRR: {return_data[4]:.2f}%\t 1M Return: {return_data[2]:.2f}%,\t Score: {return_data[3]:.2f},\t Proportion: {return_data[3] / total_s:.2f}"
        )
