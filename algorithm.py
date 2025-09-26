def bshalgorithm(data, streak_threshold=5, profit_threshold=0.05):
    signals = []
    buy_dates = []
    sell_dates = []

    data['SMA_20'] = calculate_sma(data, 20)  
    data['SMA_50'] = calculate_sma(data, 50)
    data['Streaks'] = streakindetifier(data)  
    price_now = data['Close'].iloc[i] 

    for i in range(len(data)):
        if i < 50:
            signals.append['Hold']
            continue
        sma_20 = data['SMA_20'].iloc[i]
        sma_50 = data['SMA_50'].iloc[i]
        streak = data['Streaks'].iloc[i]

        sma_20_prev = data['SMA_20'].iloc[i-1]
        sma_50_prev = data['SMA_50'].iloc[i-1]

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
            pricelowrecent = min(data['Low'].iloc[i-5:i])
            pricehighrecent = max(data['High'].iloc[i-5:i])

            if price_now > pricelowrecent*(1 + profit_threshold):
                signal = 'Buy'

            elif price_now > pricehighrecent*(1 - profit_threshold):
                signal = 'Sell'

        
        signals.append(signal)
        
        if signal == 'Buy':
            buy_dates.append(data.index[i])
            
        elif signal == 'Sell':
            sell_dates.append(data.index[i])
        
    data['Signal'] = signal
        
    return data, buy_dates, sell_dates


        

        

        
