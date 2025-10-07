import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

CSV_FILE = "MSFT.csv"
LABEL_EVERY = 50

def SMA(close, period):
    sma = []
    for i in range(len(close)):
        if i < period - 1:
            sma.append(None)
        else:
            total = sum(close[i-j] for j in range(period))
            sma.append(total / period)
    return sma

def streakIdentifier(data, period, period1):
    data['SMA'] = SMA(data['Close/Last'], period)
    data['SMA1'] = SMA(data['Close/Last'], period1)
    data = data.dropna().reset_index(drop=True)
    data.loc[:, 'Streak'] = 0

    streak = 0
    for i in range(1, len(data)):
        if data.at[i, 'SMA'] > data.at[i-1, 'SMA'] or data.at[i, 'SMA1'] > data.at[i-1, 'SMA1']:
            streak += 1
        else:
            streak -= 1
        data.at[i, 'Streak'] = streak
        
    return data

def generate_streak_chart(year=None):
    # Load CSV
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)

    # Filter by year if provided
    if year is not None:
        df = df[df['Date'].dt.year == year]

    # Compute streak
    df_streak = streakIdentifier(df, 20, 50)

    plt.figure(figsize=(12,6))
    plt.plot(df_streak['Date'], df_streak['Streak'], linewidth=1.5, color='blue', label='Streak')

    # Label every N points
    for idx in df_streak['Streak'].iloc[::LABEL_EVERY].index:
        y = df_streak['Streak'].iloc[idx]
        x = df_streak['Date'].iloc[idx]
        plt.text(x, y + 0.5, f'{y}', fontsize=8, ha='center', va='bottom')

    plt.title(f"Streak Over Time{' - ' + str(year) if year else ''}", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Streak", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), fontsize=10)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()

