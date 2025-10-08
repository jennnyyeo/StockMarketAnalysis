import pandas as pd

def daily_returns(data):
    data['Close/Last'] = data['Close/Last'].str.replace('$', '').astype(float)
    data['Open'] = data['Open'].str.replace('$', '').astype(float) 
    data['Daily Return (%)'] = (((data['Close/Last'] - data['Open']) / data['Open']) * 100).round(4)

    return data

if __name__ == "__main__":
    df = pd.read_csv('MSFT.csv')
    df = daily_returns(df)
    print(df.head(20))