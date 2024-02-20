import pandas as pd
import os
import datetime

log = open(f"logs/{datetime.datetime.now().isoformat()}.log", "w")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def test_strategy(file, START_CASH=10000, AVG_DAYS=7, AVG_GAP=2, BUY_THRESHOLD=-0.01, SELL_THRESHOLD=0.02):
    print(f"\nFile: {bcolors.UNDERLINE}{file}{bcolors.ENDC}")
    stock = file.split("-")[2]
    print(
        f"* Testing strategy on stock: {bcolors.HEADER}{stock}{bcolors.ENDC}")
    df = pd.read_csv(file)
    print(df.columns.tolist(), file=log)

    data = df.values.tolist()
    data = [[d[0], d[1], float(str(d[2]).replace(",", ""))] for d in data]

    L = len(data)

    cash = START_CASH
    stock = 0
    trades = 0
    volume = 0.00001

    for i in reversed(range(L-AVG_DAYS-AVG_GAP-1)):
        date = data[i][0]
        price = data[i][2]
        sum = 0
        for j in range(AVG_DAYS):
            sum += data[i+j+AVG_GAP+1][2]
        avg = sum / AVG_DAYS
        diff = price - avg
        print(i, date, price, avg, diff, file=log)
        if diff < BUY_THRESHOLD * avg:
            print("buy", file=log)
            if (cash > price):
                trades += 1
                cash -= 1*price
                stock += 1
                volume += price

        if diff > SELL_THRESHOLD * avg:
            print("sell", file=log)
            if (stock > 0):
                trades += 1
                cash += 1*price
                stock -= 1
                volume += price
    profit = int(cash + stock*data[0][2]) - START_CASH
    if profit > 0:
        print(
            f"--------SUCCESS ({bcolors.OKGREEN}{profit}{bcolors.ENDC})--------")
    else:
        print(
            f"--------FAILURE ({bcolors.FAIL}{profit}{bcolors.ENDC})--------")
    print(
        f">> Cash: {int(cash)}, Stock: {stock}, Asset: {int(stock*data[0][2])}, Trades: {trades}, Volume: {int(volume)}")
    print(
        f">> Profit/Volume: {bcolors.BOLD}{(100*profit/volume):.2f}%{bcolors.ENDC}")


if __name__ == "__main__":
    for path in os.listdir('data'):
        if path.endswith('.csv'):
            test_strategy(f'data/{path}',
                          START_CASH=10000,
                          AVG_DAYS=7,
                          AVG_GAP=2,
                          BUY_THRESHOLD=-0.01,
                          SELL_THRESHOLD=0.02
                          )
