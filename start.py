import pandas

data = pandas.read_csv('stock/MSFT.csv')

# format data
for x in data['Close/Last']:
    data['Close/Last']=float(x[1:])
  
print(data.info())

# 5-days SMA
data['SMA'] = data['Close/Last'].rolling(window=5).mean()
print(data) 
