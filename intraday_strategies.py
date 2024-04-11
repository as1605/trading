

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
