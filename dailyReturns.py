import pandas as pd

data = pd.read_csv('MSFT.csv')

def daily_returns(data):
    data['Close/Last'] = data['Close/Last'].str.replace('$', '').astype(float)
    data['Open'] = data['Open'].str.replace('$', '').astype(float) 
    data['Daily Return (%)'] = (data['Close/Last'] - data['Open']) / data['Open']
    
    for x in data['Daily Return (%)']:
        data['Daily Return (%)'] = data['Daily Return (%)'].round(4)
    return data

data = daily_returns(data)
print(data)