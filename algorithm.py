from streakIdentifier import streakIdentifier
import pandas as pd
import numpy as np
# from start import SMA


def bshalgorithm(data):
    signals = []
    rulesignals = []
    buy_dates = []
    sell_dates = []
    streak_threshold = 5
    profit_threshold = 0.05
    band = 0.001  # For SMA cross to prevent flicker
    q_low, q_high = 0.15, 0.85
    abs_floor = 3.0
    # ------------------ Feature From streakIdentifier.py ------------------
    ndata = data
    ndata['Date'] = pd.to_datetime(ndata['Date'], errors='coerce')
    ndata['_orig_order'] = range(len(ndata))
    ndata = ndata.sort_values(
        ['Date'], ascending=True, kind='mergesort').reset_index(drop=True)
    # ---------- Converting table values into arrays for faster loop access ------------
    sma_20list = ndata['SMA'].to_numpy()
    sma_50list = ndata['SMA1'].to_numpy()
    streaklist = ndata['StreakIdx'].astype(float).to_numpy()
    streakprevlist = ndata['StreakIdx'].shift(1).astype(float).to_numpy()
    pricelist = ndata['Close/Last'].to_numpy()
    # ----------------- Shifting the list for Prior day SMAs -----------------
    sma_20prevlist = ndata['SMA'].shift(1).to_numpy()
    sma_50prevlist = ndata['SMA1'].shift(1).to_numpy()
    # ------------------ 5-day Low/High of the previous 5 Days ------------------
    lowreclist = ndata['Low'].rolling(
        5, min_periods=5).min().shift(1).to_numpy()
    highreclist = ndata['High'].rolling(
        5, min_periods=5).max().shift(1).to_numpy()

    ql = float(np.nanquantile(streaklist, q_low))
    qh = float(np.nanquantile(streaklist, q_high))
    neg_thres = min(ql, -abs_floor)
    pos_thres = max(qh, abs_floor)

    if len(ndata) < 50:
        ndata['Signal'] = ['Hold'] * len(ndata)
        ndata = ndata.sort_values('_orig_order').drop(columns='_orig_order').reset_index(drop=True)
        return ndata, buy_dates, sell_dates

    # ------------------------ Signal Generation ------------------------
    for i in range(len(ndata)):
        sma_20 = sma_20list[i]
        sma_50 = sma_50list[i]
        streak = streaklist[i]
        streakprev = streakprevlist[i]
        price_now = pricelist[i]
        sma_20_prev = sma_20prevlist[i]
        sma_50_prev = sma_50prevlist[i]
        low5 = lowreclist[i]
        high5 = highreclist[i]

        signal = 'Hold'
        rulesignal = None

        # Rule 1: SMA Crossover
        if (sma_20 > sma_50 * (1 + band)) and (sma_20_prev <= sma_50_prev * (1 + band)):
            signal = 'Buy'
            rulesignal = 'r1buy'

        elif (sma_20 < sma_50 * (1 - band)) and (sma_20_prev >= sma_50_prev * (1 - band)):
            signal = 'Sell'
            rulesignal = 'r1sell'
        # Rule 2: Streak Reversal
        elif (streak <= neg_thres) and (streakprev > neg_thres):
            signal = 'Buy'
            rulesignal = 'r2buy'
        elif (streak >= pos_thres) and (streakprev < pos_thres):
            signal = 'Sell'
            rulesignal = 'r2sell'
        # Rule 3: Dip-buying / Profit-Taking
        elif (not pd.isna(low5)) and (sma_20 < sma_50) and (price_now >= low5 * (1 + profit_threshold)):
            signal = 'Buy'
            rulesignal = 'r3buy'
        elif (not pd.isna(high5)) and (sma_20 > sma_50) and (price_now <= high5 * (1 - profit_threshold)):
            signal = 'Sell'
            rulesignal = 'r3sell'
        signals.append(signal)
        rulesignals.append(rulesignal)

    ndata['Signal'] = signals
    ndata['RuleSignal'] = rulesignals

    ndata = ndata.sort_values('_orig_order').drop(
        columns='_orig_order').reset_index(drop=True)
    
    maxprofitresults = max_profit_dates(ndata)

    return ndata, maxprofitresults


def max_profit_dates(data):
    d = data.copy()
    d['Date'] = pd.to_datetime(d['Date'], errors='coerce')
    d = d.sort_values(['Date'], ascending=True,
                      kind='mergesort').reset_index(drop=True)
    prices = d['Close/Last']
    signals = d['Signal'].values
    dates = pd.to_datetime(d['Date'])
    max_profit = 0.0

    buy_index = None
    bestbuy_index = None
    bestsell_index = None

    for i, sig in enumerate(signals):
        if sig == 'Buy':
            if buy_index is None or (prices[i] < prices[buy_index]):
                buy_index = i

        elif sig == 'Sell':
            if buy_index is not None and i > buy_index:
                profit = prices[i] - prices[buy_index]
                if profit > max_profit:
                    max_profit = profit
                    bestbuy_index = buy_index
                    bestsell_index = i
                buy_index = None

    if bestbuy_index is None or bestsell_index is None:
        return {
            'profit': 0.0,
            'buy_date': None, 'sell_date': None,
            'buy_price': None, 'sell_price': None
        }

    return {
        'profit': round(float(max_profit), 2),
        'buy_date': dates.iloc[bestbuy_index].strftime('%Y/%m/%d'),
        'sell_date': dates.iloc[bestsell_index].strftime('%Y/%m/%d'),
        'buy_price': round(float(prices.iloc[bestbuy_index]), 2),
        'sell_price': round(float(prices.iloc[bestsell_index]), 2)
    }


# df = pd.read_csv('MSFT.csv')
# for col in ['Close/Last', 'High', 'Low']:
#     df[col] = df[col].str.replace('$', '').astype(float)
# ndata, buy_dates, sell_dates, maxprofit = bshalgorithm(df)
# ndata.to_csv('ndata.csv', index=False)
# print(maxprofit)
