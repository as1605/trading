from datetime import timedelta
from jugaad_data import nse

from indices.symbols import NIFTY50, NIFTY500, NIFTYTOTALMARKET
from intraday_strategies import marubuzo
from intraday_strategies import hammer
from intraday_strategies import hanging_man
from intraday_utils import get_ohlc, split_graph_to_candlesticks
from strategy import bcolors

jugaad = nse.NSELive()


def fetch(stock: str):
    data = jugaad.chart_data(stock)
    graph = data['grapthData']

    candlesticks = split_graph_to_candlesticks(graph, timedelta(minutes=2))

    return graph, candlesticks


def explore(stock: str):
    print("*"*80)
    print("Exploring", stock)
    graph, candlesticks = fetch(stock)

    print("Graph has", len(graph), "entries")
    get_ohlc(graph, display=True)
    print("There are", len(candlesticks), "candlesticks")
    print("Opening candlestick", candlesticks[0])
    print("Closing candlestick", candlesticks[-1])

    print("0-5 Candlesticks")
    for candlestick in candlesticks[:5]:
        get_ohlc(candlestick, display=True)

    print("50-55 Candlesticks")
    for candlestick in candlesticks[50:55]:
        get_ohlc(candlestick, display=True)


explore("RELIANCE")

for stock in NIFTY50:
    print("*"*40, bcolors.BOLD, stock, bcolors.ENDC, "*"*(40-len(stock)))
    try:
        g, candlesticks = fetch(stock)
    except Exception as e:
        print("Failed to fetch")
        continue
    # try:
    #     print("Full Day")
    #     get_ohlc(g, display=True)
    #     print("Last Candlestick")
    #     get_ohlc(c[-1], display=True)
    # except Exception as e:
    #     print("Failed to display")
    #     continue

    # Checking last 10 candlesticks (20 minutes) only
    for i in range(10):
        last = candlesticks[-i-1]
        if i == 0:
            window = candlesticks[-10:]
        else:
            window = candlesticks[-i-10:-i]
        if marubuzo(candlesticks[-i-1], 0.01, 0.1):
            print("Marubuzo found!", end=" ")
            get_ohlc(candlesticks[-i-1], display=True)
        if hammer(window, 0.01, 0.05):
            print("Hammer found!", end=" ")
            get_ohlc(window, display=True)
        if hanging_man(window, 0.01, 0.05):
            print("Hanging Man found!", end=" ")
            get_ohlc(window, display=True)
