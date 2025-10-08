# import pandas
# if __name__ == "__main__":
#     data = pandas.read_csv('MSFT.csv')

# # Empty list to store cleaned values
# cleaned = []

# cleaned = [float(x[1:]) for x in data['Close/Last']]    # list comprehension


# data['Close/Last'] = cleaned
# print(data.info())

# period = input('select SMA days(must be integer):')
# if period.isdigit() and 2<=int(period)<=len(data):
#     period = int(period)
# else:
#     print('your input is invalid select 2 or more days without exceeding data series')
#     exit()

# function annotation
def SMA(close:float,period:int):
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
     

# data['custom_SMA']=SMA(data['Close/Last'],5)    #positional argument

# # test validation
# data['test_SMA'] = data['Close/Last'].rolling(window=5).mean()
# print(data)