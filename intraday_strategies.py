

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


def hammer(candlesticks: list[list[tuple[int, float]]], tolerance=0.1, mincp=0.1) -> bool:
    if len(candlesticks) < 2:
        return False
    candlestick = candlesticks[-1]
    prev = candlesticks[-2]
    prev_open, prev_high, prev_low, prev_close, prev_change, prev_cp = get_ohlc(
        prev, display=False)
    

    if bullish_hammer(candlestick, tolerance, mincp) or bearish_hammer(candlestick, tolerance, mincp):
        return True
    return False


def bullish_hammer(candlestick: list[tuple[int, float]], tolerance: float, mincp: float) -> bool:
    open, high, low, close, change, cp = get_ohlc(candlestick, display=False)

    if abs(cp) > mincp:
        if (close > open) and 2*(close-open) <= (open-low):
            if abs(close-high) < tolerance * abs(cp):
                return True

    return False


def bearish_hammer(candlestick: list[tuple[int, float]], tolerance: float, mincp: float) -> bool:
    open, high, low, close, change, cp = get_ohlc(candlestick, display=False)

    if abs(cp) > mincp:
        if (open > close) and 2*(open-close) <= (close-low):
            if abs(open-high) < tolerance * abs(cp):
                return True

    return False


def hanging_man(candlestick: list[tuple[int, float]], tolerance=0.1, mincp=0.1) -> bool:
    if bullish_hanging_man(candlestick, tolerance, mincp) or bearish_hanging_man(candlestick, tolerance, mincp):
        return True
    return False


def bullish_hanging_man(candlestick: list[tuple[int, float]], tolerance: float, mincp: float) -> bool:
    open, high, low, close, change, cp = get_ohlc(candlestick, display=False)

    if abs(cp) > mincp:
        if (close > open) and 2*(close-open) <= (open - low):  # bullish hanging man
            if abs(close-high) < tolerance*abs(change):
                return True

    return False


def bearish_hanging_man(candlestick: list[tuple[int, float]], tolerance: float, mincp: float) -> bool:
    open, high, low, close, change, cp = get_ohlc(candlestick, display=False)

    if abs(cp) > mincp:
        if (open > close) and 2*(open-close) <= (close-low):  # bearish hanging man
            if abs(open-high) < tolerance * abs(change):
                return True

    return False
