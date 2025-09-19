import pandas

data = pandas.read_csv('MSFT.csv')

# Empty list to store cleaned values
cleaned = []

for x in data['Close/Last']:
    cleaned.append(float(x[1:]))   # remove '$' and convert to float

data['Close/Last'] = cleaned
print(data.info())




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
     

data['custom_SMA']=SMA(data['Close/Last'],5) 
# test validation
data['test_SMA'] = data['Close/Last'].rolling(window=5).mean()
print(data)