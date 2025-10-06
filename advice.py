import pandas as pd

def give_advice_text(ndata: pd.DataFrame, streak_warn: int = 5) -> str:
    latest = ndata.iloc[-1]
    signal = latest['Signal']
    streak = latest['Streak']

    lines = []
    lines.append("=== Trading Advice ===")
    lines.append(f"Signal = {signal.upper()} | Streak = {streak}\n")

    if signal == "Buy":
        lines.append("BUY!!! The model thinks the price may go up soon.\n")
        lines.append("Beginner Tips:")
        lines.append("  - Don’t spend all your money at once. Start small.")
        lines.append("  - Always use a stop-loss in case the trade goes wrong.\n")

    elif signal == "Sell":
        lines.append("SELL!!! The model thinks the price may go down soon.\n")
        lines.append("Beginner Tips:")
        lines.append("  - It is safer to take your money out here instead of waiting.")
        lines.append("  - Do not let emotions (fear or greed) control your decision.\n")

    else:  # Hold
        lines.append("HOLD!!! The model sees no clear direction right now.\n")
        lines.append("Beginner Tips:")
        lines.append("  - The best action may be doing nothing and waiting.")
        lines.append("  - Be patient — forcing trades often leads to losses.\n")

    if streak >= streak_warn:
        lines.append("⚠️ Streak Warning: ⚠️")
        lines.append(f"- The price has gone UP for {streak} days in a row.")
        lines.append("- Often after many up days, the price may fall back (pullback).\n")
        lines.append("Beginner Tips:")
        lines.append("  - Think about taking some profit instead of buying more.\n")

    elif streak <= -streak_warn:
        lines.append("⚠️ Streak Warning: ⚠️")
        lines.append(f"- The price has gone DOWN for {streak} days in a row.")
        lines.append("- This could mean overselling, so a bounce is possible.\n")
        lines.append("Beginner Tips:")
        lines.append("  - Be patient and don’t rush in with too much money at once.\n")

    lines.append("\n===================== General Beginner Warnings ====================")
    lines.append("1. ❌ Avoid anchors → Don’t just follow one indicator blindly (like SMA). Confirm with other signals.")
    lines.append("2. ❌ Avoid cheap stocks → Cheap does not mean good; they can be traps.")
    lines.append("3. ❌ Avoid predictions → Nobody can guarantee the next move. Stick to your plan.")
    lines.append("4. ❌ Avoid 'multibagger' hype → Be careful of stocks hyped as 'next big thing'.")
    lines.append("5. ❌ Avoid random stock tips → If you didn’t research it, don’t trade it.")

    lines.append("\n========================= Concepts To Know =========================")
    lines.append("- Moving Averages → Helps to smooth out price trends over time.")
    lines.append("- Business Cycle → Prices move in cycles: fear vs. greed.")
    lines.append("- Diversification → Spreading investments reduces risk.")
    lines.append("- Price of Stock → Always check if it’s overpriced or underpriced.")
    lines.append("- Types of Orders → Learn Stop-loss, Limit orders, etc.")

    lines.append("\n=================== Common Risks in Stock Market ====================")
    lines.append("- Inflation → Can reduce investor confidence.")
    lines.append("- Slowdown in GDP → Makes many companies overvalued.")
    lines.append("- Panic Selling → When fear spreads, prices can crash quickly.")
    lines.append("- High Leverage → Borrowing too much to trade magnifies risk.")

    return "\n".join(lines)

## this is just for my testingm, can remove this 
'''if __name__ == "__main__":
    import pandas as pd
    from algorithm import bshalgorithm

    # Load sample data (MSFT.csv)
    df = pd.read_csv("MSFT.csv")
    for col in ["Close/Last", "High", "Low"]:
        df[col] = df[col].astype(str).str.replace("$", "", regex=False).astype(float)

    # Run algorithm to generate signals
    ndata, buy_dates, sell_dates = bshalgorithm(df)

    print("\n=== Text Version Output (for Flask) ===")
    print(give_advice_text(ndata))   # prints the returned text string '''
