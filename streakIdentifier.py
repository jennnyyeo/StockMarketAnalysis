import pandas as pd
import numpy as np

def SMA(close,period):
    sma=[]
    
    for i in range(len(close)):
        if i<period-1: #index 0-3
            sma.append(None)
        else:   # index 4
            total=0
            for j in range(period):
                total+=close[i-j] 
            sma.append(total/period)   
    return sma

def streakIdentifier(data, period, period1):
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    data['_orig_order'] = range(len(data))
    data = data.sort_values(['Date'], ascending=True, kind='mergesort').reset_index(drop=True)
    data['SMA'] = SMA(data['Close/Last'], period)
    data['SMA1'] = SMA(data['Close/Last'], period1)
    data = data.dropna().reset_index(drop=True)
    data.loc[:, 'Streak'] = 0
    streak = 0
    for i in range(1, len(data)):
        if data.at[i, 'SMA'] > data.at[i-1, 'SMA'] or data.at[i, 'SMA1'] > data.at[i-1, 'SMA1']:
            streak += 1
        else:
            streak -= 1
        data.at[i, 'Streak'] = streak
    data = data.sort_values('_orig_order').drop(columns='_orig_order').reset_index(drop=True)   
    return data


df = pd.read_csv('MSFT.csv')
df['Close/Last'] = df['Close/Last'].str.replace('$', '').astype(float)
result = streakIdentifier(df, 20, 50)

print(result)