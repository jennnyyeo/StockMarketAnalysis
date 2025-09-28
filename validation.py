import pandas as pd
from start import SMA   # import SMA function

# loads dataset
data = pd.read_csv("MSFT.csv")
cleaned = []
for x in data['Close/Last']:
    cleaned.append(float(x[1:]))  # skip the first character ($)
data['Close/Last'] = cleaned


# ask for period
period = int(input("Select SMA days: "))

# compares custom (from start.py) and built-in rolling mean
data['custom_SMA'] = SMA(data['Close/Last'], period)
data['test_SMA']   = data['Close/Last'].rolling(window=period).mean()


ok = data['custom_SMA'].round(5).equals(data['test_SMA'].round(5)) # rounds value to 5dp


# print results
print("\n=== Validation Result (SMA) ===")
print(f"Window: {period} | Result: {'PASS' if ok else 'FAIL'}")  
print(data[['Close/Last','custom_SMA','test_SMA']].tail(15))
