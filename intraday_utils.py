
import datetime


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


def convert_time(t: int):
    return datetime.datetime.fromtimestamp(t//1000 - 5.5*60*60).strftime('%H:%M:%S')


def get_ohlc(candlestick: list[tuple[int, int]], display=False):
    o = candlestick[0][1]
    c = candlestick[-1][1]
    h = max(candlestick, key=lambda x: x[1])[1]
    l = min(candlestick, key=lambda x: x[1])[1]
    if display:
        if c > o:
            print(bcolors.OKGREEN, end="")
        if c < o:
            print(bcolors.FAIL, end="")
        print(
            f"{convert_time(candlestick[0][0])}-{convert_time(candlestick[-1][0])}: Open:{o:8.2f} | High:{h:8.2f} | Low:{l:8.2f} | Close:{c:8.2f} | Change:{c-o:8.2f} | Change%:{(c-o)/o*100: 4.2f}")
        print(bcolors.ENDC, end="")
    return (o, h, l, c, c-o, (c-o)/o*100)


def split_graph_to_candlesticks(graph: list[tuple[int, int]], time: datetime.timedelta = datetime.timedelta(minutes=5)):
    candlesticks = []
    candlestick = []
    for tp in graph:
        if candlestick == []:
            candlestick = [tp]
        elif tp[0] - candlestick[0][0] < time.total_seconds() * 1000:
            candlestick.append(tp)
        else:
            candlesticks.append(candlestick)
            candlestick = [tp]
    return candlesticks
