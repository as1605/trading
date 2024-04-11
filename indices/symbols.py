import pandas as pd


def get_symbols(file):
    df = pd.read_csv(file)
    return df['Symbol'].tolist()


NIFTY50 = get_symbols('indices/ind_nifty50list.csv')
NIFTY500 = get_symbols('indices/ind_nifty500list.csv')
NIFTYTOTALMARKET = get_symbols('indices/ind_niftytotalmarket_list.csv')
