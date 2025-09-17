import pandas

data = pandas.read_csv('MSFT.csv')
print(data)
# format data
data['Close/Last'] = data['Close/Last'].str.replace('$', '').astype(float)

print(data.info())

# 5-days SMA
data['SMA'] = data['Close/Last'].rolling(window=5).mean().round(4)
for i in range(20):
    print(data['Date'].iloc[i], data['SMA'].iloc[i])