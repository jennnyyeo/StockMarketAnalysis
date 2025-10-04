from streakIdentifier import streakIdentifier
import pandas as pd
# from start import SMA

def bshalgorithm(data):
    signals = []
    buy_dates = []
    sell_dates = []
    streak_threshold=5
    profit_threshold=0.05
    ndata = streakIdentifier(data, 20, 50)
    sma_20list = ndata['SMA']  
    sma_50list = ndata['SMA1']   
    print(len(ndata))

    for i in range(len(ndata)):
        if len(ndata) < 50:
            signals.append('Hold')
            continue
        else:
            sma_20 = sma_20list.iloc[i]
            sma_50 = sma_50list.iloc[i]
            streak = ndata['Streak'].iloc[i]
            price_now = ndata['Close/Last'].iloc[i]
            
            sma_20_prev = sma_20list.iloc[i-1]
            sma_50_prev = sma_50list.iloc[i-1]

            signal = 'Hold'

            #Rule 1: SMA Crossover  
            if sma_20 > sma_50 and sma_20_prev <= sma_50_prev:
                signal = 'Buy'

            elif sma_20 < sma_50 and sma_20_prev >= sma_50_prev:
                signal = 'Sell'
                
            #Rule 2: Streak Reversal
            elif streak <= -streak_threshold:
                signal = 'Buy'

            elif streak >= streak_threshold:
                signal = 'Sell'
                
            #Rule 3: Dip-buying / Profit-Taking 
            elif i > 5:
                pricelowrecent = min(ndata['Low'].iloc[i-5:i])
                pricehighrecent = max(ndata['High'].iloc[i-5:i])

                if price_now > pricelowrecent*(1 + profit_threshold):
                    signal = 'Buy'

                elif price_now > pricehighrecent*(1 - profit_threshold):
                    signal = 'Sell'

            
            signals.append(signal)
            
            if signal == 'Buy':
                buy_dates.append(ndata['Date'].iloc[i])
                
            elif signal == 'Sell':
                sell_dates.append(ndata['Date'].iloc[i])
            
    ndata['Signal'] = signals
        
    return ndata, buy_dates, sell_dates


df = pd.read_csv('MSFT.csv')
for col in ['Close/Last', 'High', 'Low']:
    df[col] = df[col].str.replace('$', '').astype(float)
       
ndata, buy_dates, sell_dates = bshalgorithm(df)



        
