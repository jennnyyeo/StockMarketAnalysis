import pandas
from advice import sma_risk_tips 

data = pandas.read_csv('MSFT.csv')

'''
corner cases, such as when the data series is shorter than
the SMA window, or when one day’s data is missing.
'''
# Empty list to store cleaned values
cleaned = []

for x in data['Close/Last']:
    cleaned.append(float(x[1:]))   # remove '$' and convert to float

data['Close/Last'] = cleaned
# print(data.info())

period = input('select SMA days(must be integer):')
if period.isdigit() and 2<=int(period)<=len(data):
    period = int(period)
else:
    print('your input is invalid select 2 or more days without exceeding data series')
    exit()

# period 2 to last day


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
     

data['custom_SMA']=SMA(data['Close/Last'],period) 
# test validation
data['test_SMA'] = data['Close/Last'].rolling(window=period).mean()
print(data)

sma_risk_tips(data, 5)