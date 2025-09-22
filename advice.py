# advice.py
## this code prints risk management advice based on the most recent close vs sma
## and it looks at the newest row that has a valid sma
def sma_risk_tips(data, window=5): 

    # get the latest row with a valid SMA
    latest_row = data[data['custom_SMA'].notna()].iloc[0] 

    latest_date  = str(latest_row.iloc[0]) 
    latest_close = latest_row['Close/Last']
    latest_sma   = latest_row['custom_SMA']

    print("\n=== Risk Management Tips (Based on SMA) ===")
    print(f"Date: {latest_date}")
    # Calculate % difference between Close and SMA
    diff = abs(latest_close - latest_sma) / latest_sma

    # Neutral zone: Close is within ±1% of SMA
    if diff < 0.01:
        print(f"Today’s Close {latest_close:.2f} is VERY CLOSE to SMA({window}) {latest_sma:.2f}.")
        print("The trend is unclear right now (neutral zone).")
        print("- Avoid rushing into trades; better to wait for confirmation.")
        print("- Manage risk carefully — no strong signal yet.")
    # uptrend
    elif latest_close > latest_sma:
        print(f"Today’s Close {latest_close:.2f} is ABOVE SMA({window}) {latest_sma:.2f}.")
        print("The stock is stronger than its recent trend (uptrend).")
        print("- Don’t get overconfident — avoid chasing prices.")
        print("- Stick to your stop-loss to prevent emotional trading.")
        print("- Take profits gradually; avoid overtrading.")
    #downtrend
    else:
        print(f"Today’s Close {latest_close:.2f} is BELOW SMA({window}) {latest_sma:.2f}.")
        print("The stock is weaker than its recent trend (downtrend).")
        print("- Don’t panic sell — follow your plan calmly.")
        print("- Avoid revenge trading or trying to catch the bottom.")
        print("- Focus on protecting capital until the trend stabilizes.")
