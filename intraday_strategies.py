

from intraday_utils import get_ohlc


def marubuzo(candlestick: list[tuple[int, float]], tolerance=0.1, mincp=0.1) -> bool:
    if bullish_marubuzo(candlestick, tolerance, mincp) or bearish_marubuzo(candlestick, tolerance, mincp):
        return True
    return False


def bullish_marubuzo(candlestick: list[tuple[int, float]], tolerance: float, mincp: float) -> bool:
    open, high, low, close, change, cp = get_ohlc(candlestick, display=False)
    if abs(cp) > mincp:
        if high - close < tolerance * abs(change):
            if open - low < tolerance * abs(change):
                return True
    return False


def bearish_marubuzo(candlestick: list[tuple[int, float]], tolerance: float, mincp: float) -> bool:
    open, high, low, close, change, cp = get_ohlc(candlestick, display=False)
    if abs(cp) > mincp:
        if high - open < tolerance * abs(change):
            if close - low < tolerance * abs(change):
                return True
    return False


def hammer(candlestick: list[tuple[int, float]], tolerance: float, mincp: float) -> bool:
    open, high, low, close, change, cp = get_ohlc(candlestick, display=False)

    # check for previous downtrend
    # if len(candlestick) < 3:
    #     return False
    # prev_open = candlestick[][]  # previous open price
    # prev_close = candlestick[][]  # previous close price

    # prev_prev_close = candlestick[][]  # previous close price
    # prev_prev_open = candlestick[][]  # previous open price

    # if prev_close < prev_open and prev_prev_close < prev_prev_open:

    if (close > open) and 2*(close-open) <= (open-low):     # bullish hammer
        if abs(close-high) < tolerance*abs(change):
            return True

    if (open > close) and 2*(open-close) <= (close-low):  # bearish hammer
        if abs(open-high) < tolerance * abs(change):
            return True
    return False


def hanging_man(candlestick: list[tuple[int, float]], tolerance: float, mincp: float) -> bool:
    open, high, low, close, change, cp = get_ohlc(candlestick, display=False)
    # check for previous uptrend
    # if len(candlestick) < 3:
    #     return False
    # prev_close = candlestick[-2][1]  # previous close price
    # prev_open = candlestick[-2][0]  # previous open price
    # prev_prev_close = candlestick[-3][1]  # previous close price
    # prev_prev_open = candlestick[-3][0]  # previous open price
    # if prev_close > prev_open and prev_prev_close > prev_prev_open:

    if (close > open) and 2*(close-open) <= (open-low):  # bullish hanging man
        if abs(close-high) < tolerance*abs(change):
            return True

    if (open > close) and 2*(open-close) <= (close-low):  # bearish hanging man
        if abs(open-high) < tolerance * abs(change):
            return True
    return False
