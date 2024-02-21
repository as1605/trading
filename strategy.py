import pandas as pd
import os
import datetime
from matplotlib import pyplot as plt

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
    print(f"\nFile: {bcolors.UNDERLINE}{file}{bcolors.ENDC}", file=log)
    stock = file.split("/")[1].split("-")[0]
    print(
        f"* Testing strategy on stock: {bcolors.HEADER}{stock}{bcolors.ENDC}", file=log)
    df = pd.read_csv(file)
    print(df.columns.tolist(), file=log)

    data = df.values.tolist()
    data = [[d[0], d[1], float(str(d[8]).replace(",", ""))] for d in data]

    L = len(data)
    # plt.plot([d[2] for d in data])
    # plt.show()

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
            f"--------SUCCESS ({bcolors.OKGREEN}{profit}{bcolors.ENDC})--------", file=log)
    else:
        print(
            f"--------FAILURE ({bcolors.FAIL}{profit}{bcolors.ENDC})--------", file=log)
    print(
        f">> Cash: {int(cash)}, Stock: {stock}, Asset: {int(stock*data[0][2])}, Trades: {trades}, Volume: {int(volume)}", file=log)
    print(
        f":: Profit/Volume: {bcolors.BOLD}{(100*profit/volume):.2f}%{bcolors.ENDC}", file=log)
    return profit, cash


def run_all(data_dir="data", start_cash=10000, avg_days=7, avg_gap=2, buy_threshold=-0.01, sell_threshold=0.02):
    total_profit = 0
    total_cash = 0
    initial_cash = 0

    for path in os.listdir(data_dir):
        if path.endswith('.csv'):
            initial_cash += start_cash
            p, c = test_strategy(f'{data_dir}/{path}',
                                 START_CASH=start_cash,
                                 AVG_DAYS=avg_days,
                                 AVG_GAP=avg_gap,
                                 BUY_THRESHOLD=buy_threshold,
                                 SELL_THRESHOLD=sell_threshold
                                 )
            total_profit += p
            total_cash += c
    print(
        f"Initial cash: {bcolors.BOLD}{bcolors.UNDERLINE}{bcolors.OKCYAN}{initial_cash:.2f}{bcolors.ENDC}")
    print(
        f"Margin: {bcolors.BOLD}{bcolors.UNDERLINE}{bcolors.OKCYAN}{100*total_cash/initial_cash:.2f}%{bcolors.ENDC}")
    print(
        f"Total profit: {bcolors.BOLD}{bcolors.UNDERLINE}{bcolors.OKCYAN}{100*total_profit/initial_cash:.2f}%{bcolors.ENDC}\n\n")
    return total_cash, total_profit, initial_cash


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print(f"Starting strategy test at {start_time}")

    x = []
    y1 = []
    y2 = []

    for rate in range(0, 100):
        print(f"Optimizing @rate={rate/10:.1f}")
        c, p, i = run_all(buy_threshold=-rate/1000,
                          sell_threshold=2*rate/1000, start_cash=15000)
        x.append(rate/10)
        y1.append(c/i)
        y2.append(p/i)

    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()

    end_time = datetime.datetime.now()
    print(f"Time Taken: {end_time-start_time} s")
