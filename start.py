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