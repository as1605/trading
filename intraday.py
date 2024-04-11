from datetime import timedelta
from jugaad_data import nse

from indices.symbols import NIFTY50, NIFTY500, NIFTYTOTALMARKET
from intraday_strategies import marubuzo
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
        g, c = fetch(stock)
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

    for candlestick in c:
        if marubuzo(candlestick, 0.01, 0.2):
            print("Marubuzo found!", end=" ")
            get_ohlc(candlestick, display=True)
