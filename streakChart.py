import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from streakIdentifier import streakIdentifier

# Default CSV file and label interval
CSV_FILE = "MSFT.csv"
# Show labels on every 50th data point for readability
LABEL_EVERY = 10

def generate_streak_chart(data, year=None, ticker="MSFT"):
    df = data.copy()
    # Clean Close/Last column
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)
    
    # Sort by date to ensure chronological order
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Compute streaks on full dataset
    df_streak = streakIdentifier(df)

    # Filter by year if provided
    if year is not None and year != "All":
        df_streak = df_streak[df_streak['Date'].dt.year == int(year)].reset_index(drop=True)
    
    # Handle empty dataset
    if df_streak.empty:
        plt.figure(figsize=(12,6))
        plt.text(0.5, 0.5, f"No data for {ticker} in year {year}", 
                 ha='center', va='center', fontsize=16)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.getvalue()

    # Plot streak
    plt.figure(figsize=(12,6))
    plt.plot(df_streak['Date'], df_streak['Streak'], linewidth=1.5, color='blue', label='Streak')

    # Label every 10th point on the streak line
    for idx in df_streak.iloc[::LABEL_EVERY].index:
        y = df_streak['Streak'].iloc[idx]
        if pd.notna(y):
            x = df_streak['Date'].iloc[idx]
            plt.text(x, y+3, f'{y}', fontsize=8, ha='center', va='bottom', color='blue')

    # Titles and labels
    plt.title(f"{ticker} Streak Over Time{' - ' + str(year) if year else ''}", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Streak", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), fontsize=10)
    plt.tight_layout()

    # Save to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()