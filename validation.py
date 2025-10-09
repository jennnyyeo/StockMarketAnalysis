import pandas as pd
import numpy as np
from start import SMA
from dailyReturns import daily_returns
from streakIdentifier import streakIdentifier
from algorithm import bshalgorithm  

# load dataset
raw = pd.read_csv("MSFT.csv")

# For SMA and StreakIdentifier the Close/Last needs to be float, remove the $
close_floats = raw.copy()
close_floats["Close/Last"] = close_floats["Close/Last"].astype(str).str.lstrip("$").astype(float)

# For daily_returns() needs the '$' as strings
strings_close_open = raw.copy()
strings_close_open["Close/Last"] = strings_close_open["Close/Last"].astype(str)
strings_close_open["Open"]       = strings_close_open["Open"].astype(str)

# For algorithm / max profit the Close/Last, High, Low needs to be float
'''algo_floats = raw.copy()
for col in ["Close/Last", "High", "Low"]:
    algo_floats[col] = algo_floats[col].astype(str).str.lstrip("$").astype(float)'''

# SMA VALIDATION using built-in rolling mean
print("="*20 + "SMA Validation" + "="*20)
sma_results = [] # collects pass/fail per window (5,10,20)
for period in [5, 10, 20]: # test the period 5 10 and 20
    close_floats[f"custom_SMA_{period}"] = SMA(close_floats["Close/Last"], period) # sma from start
    close_floats[f"ref_SMA_{period}"]    = close_floats["Close/Last"].rolling(window=period).mean() # validating against the built in rolling mean
    ok = pd.Series(close_floats[f"custom_SMA_{period}"]).round(5).equals(
         close_floats[f"ref_SMA_{period}"].round(5))
    sma_results.append(ok) # append the result for this window
    print(f"\n=== Validation Result (SMA {period}) ===  {'PASS' if ok else 'FAIL'}")
    print(close_floats[["Close/Last", f"custom_SMA_{period}", f"ref_SMA_{period}"]].tail(5))

ok_sma_all = all(sma_results) # this will only pass if all windows (5,10,15) passed
print()

# StreakIdentifier VALIDATION based on SMA
print("="*12 + "StreakIdentifier Validation (SMA Based)" + "="*12)
streakdf = close_floats.copy()
streakdf['SMA'] = SMA(streakdf['Close/Last'], 20)
streakdf['SMA1'] = SMA(streakdf['Close/Last'], 50)

##print("Cols before call:", streakdf.columns.tolist()) i used to check the columns
##print(streakdf[["Close/Last","SMA","SMA1"]].head(3))
ndata = streakIdentifier(streakdf) # from streakidentifier() function

# building references in chronological order
t = ndata.sort_values("Date").reset_index(drop=True) # sorted by the date column
ref = [0] # streak starts at 0
for i in range(1, len(t)): # step through days
    up   = (t["SMA"].iloc[i]  > t["SMA"].iloc[i-1]) or (t["SMA1"].iloc[i] > t["SMA1"].iloc[i-1])
    down = (t["SMA"].iloc[i]  < t["SMA"].iloc[i-1]) or (t["SMA1"].iloc[i] < t["SMA1"].iloc[i-1])
    if up:
        ref.append(ref[-1] + 1) # increase streak if either SMA rises
    elif down:
        ref.append(ref[-1] - 1) # decrease streak if either SMA falls
    else:
        ref.append(ref[-1]) # no change

ok_streak = t["Streak"].astype(int).equals(pd.Series(ref)) # comparing against the streakidentifier()
print(f"Validation Result: {'PASS' if ok_streak else 'FAIL'}")
print(t[["Date","SMA","SMA1","Streak"]].head(10))

#  Daily Returns VALIDATION (intraday %)
print("="*12 + "DailyReturns Validation" + "="*12)
dr_out = daily_returns(strings_close_open.copy()) # running daily_returns()
ref_intraday_pct = (((dr_out["Close/Last"] - dr_out["Open"]) / dr_out["Open"]) * 100).round(4) # calculates the difference between the closing price and the opening price of the stock on the same day.
# if this is positive, it measn the stock price went up and if this is negative, it means the stock price went down
ok_intraday = dr_out["Daily Return (%)"].equals(ref_intraday_pct) # validating against the daily_returns()
print(f"Validation Result (daily_returns vs (Close-Open)/Open * 100): {'PASS' if ok_intraday else 'FAIL'}")
print(dr_out[["Date","Close/Last","Open","Daily Return (%)"]].head(12))
print()

#  Max Profit Validation
print("="*12 + " Max Profit (Single Trade via Signals) Validation " + "="*12)
ndata_algo, buy_dates, sell_dates, maxprofit_result = bshalgorithm(algo_floats.copy())
# this is for reference check 
d = ndata_algo.copy()
d["Date"] = pd.to_datetime(d["Date"], errors="coerce")
d = d.sort_values("Date").reset_index(drop=True)
# track the cheapest Buy so far; on Sell, evaluate profit; then reset (match your function)
best_profit = 0.0
best = {"profit": 0.0, "buy_date": None, "sell_date": None, "buy_price": None, "sell_price": None}
min_buy_price = None
min_buy_date  = None

for _, r in d.iterrows():
    sig, p, dt = r["Signal"], float(r["Close/Last"]), r["Date"]
    if sig == "Buy":
        if (min_buy_price is None) or (p < min_buy_price):
            min_buy_price, min_buy_date = p, dt # choose cheapest buy so far
    elif sig == "Sell" and (min_buy_price is not None):
        prof = p - min_buy_price  # candidate profit
        if prof > best_profit: # keep best pair
            best_profit = prof
            best = {
                "profit": round(prof, 2),
                "buy_date": min_buy_date.strftime("%Y/%m/%d"),
                "sell_date": dt.strftime("%Y/%m/%d"),
                "buy_price": round(min_buy_price, 2),
                "sell_price": round(p, 2),
            }
        min_buy_price = None # require a new buy after selling
        min_buy_date  = None

ok_mp = (
    float(maxprofit_result.get("profit", 0.0)) == float(best.get("profit", 0.0))
    and maxprofit_result.get("buy_date")  == best.get("buy_date")
    and maxprofit_result.get("sell_date") == best.get("sell_date")
    and (maxprofit_result.get("buy_price")  is None or round(float(maxprofit_result["buy_price"]),  2) == best["buy_price"])
    and (maxprofit_result.get("sell_price") is None or round(float(maxprofit_result["sell_price"]), 2) == best["sell_price"])
)
print("Your max_profit_dates:", maxprofit_result)
print("Ref  (one-pass)     :", best)
print(f"Validation (max_profit_dates vs one-pass): {'PASS' if ok_mp else 'FAIL'}")
print()

#  Corner Cases (SMA) given inside the project
print("="*12 + "Corner Case: SMA shorter than window" + "="*12)
short_data = pd.DataFrame({"Close/Last": [100, 102, 105]}) # only 3 points
short_sma = SMA(short_data["Close/Last"], 5) # start.py returns a list with None for early rows
short_ref = short_data["Close/Last"].rolling(window=5).mean() # built in rolling mean will return NaN for early rows
short_sma_converted = pd.Series([np.nan if v is None else v for v in short_sma]) # none and nan comparison
ok_short = short_sma_converted.equals(short_ref) # validating
print(f"Validation Result (SMA shorter than window): {'PASS' if ok_short else 'FAIL'}")

print("\n" + "="*12 + "Corner Case: SMA with missing data" + "="*12)
nan_data = pd.DataFrame({"Close/Last": [100, np.nan, 104, 106, np.nan, 110]})
nan_sma = SMA(nan_data["Close/Last"], 3)
nan_ref = nan_data["Close/Last"].rolling(window=3).mean()
nan_sma_converted = pd.Series([np.nan if v is None else v for v in nan_sma])
ok_nan = nan_sma_converted.equals(nan_ref)
print(f"Validation Result (SMA with missing data): {'PASS' if ok_nan else 'FAIL'}")

# Summary and Excel 
print("\n" + "="*25 + "Summary" + "="*25)
print(f"SMA (5/10/20): {'PASS' if ok_sma_all else 'FAIL'}")
print(f"StreakIdentifier: {'PASS' if ok_streak else 'FAIL'}")
print(f"DailyReturns: {'PASS' if ok_intraday else 'FAIL'}")
print(f"Max Profit (single trade via signals): {'PASS' if ok_mp else 'FAIL'}")
print(f"SMA < window corner case: {'PASS' if ok_short else 'FAIL'}")
print(f"SMA with NaNs corner case: {'PASS' if ok_nan else 'FAIL'}")

# Export summary to Excel
summary = {
    "SMA (5/10/20)": "PASS" if ok_sma_all else "FAIL",
    "StreakIdentifier": "PASS" if ok_streak else "FAIL",
    "DailyReturns": "PASS" if ok_intraday else "FAIL",
    "Max Profit (single trade via signals)": "PASS" if ok_mp else "FAIL",
    "SMA < window corner case": "PASS" if ok_short else "FAIL",
    "SMA with NaNs corner case": "PASS" if ok_nan else "FAIL",
}
pd.DataFrame(list(summary.items()), columns=["Test Case", "Result"])\
  .to_excel("validation_results.xlsx", index=False, engine="openpyxl") # write to excel
print("\nValidation results exported to Excel: validation_results.xlsx")
