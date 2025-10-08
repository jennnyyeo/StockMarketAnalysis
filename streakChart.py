import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from streakIdentifier import streakIdentifier


CSV_FILE = "MSFT.csv"

def generate_streak_chart(data, year=None):
    # Load and clean CSV
    # df = pd.read_csv(CSV_FILE)
    # df['Date'] = pd.to_datetime(df['Date'])
    df = data
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)

    # Sort chronologically (oldest first)
    df = df.sort_values('Date').reset_index(drop=True)

    # Compute streak on full dataset
    df_streak = streakIdentifier(df)

    # Filter by year **after computing streak**
    if year is not None and year != "All":
        df_streak = df_streak[df_streak['Date'].dt.year == int(year)].reset_index(drop=True)

    # Handle empty filtered dataset
    if df_streak.empty:
        plt.figure(figsize=(12,6))
        plt.text(0.5, 0.5, f"No data for year {year}", ha='center', va='center', fontsize=16)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        return buf.getvalue()

    # Plot streak chart
    plt.figure(figsize=(12,6))
    plt.plot(df_streak['Date'], df_streak['Streak'], linewidth=1.5, color='blue', label='Streak')

    # Highlight highest streak point in the filtered data
    max_idx = df_streak['Streak'].idxmax()
    x_max = df_streak['Date'].iloc[max_idx]
    y_max = df_streak['Streak'].iloc[max_idx]
    plt.scatter(x_max, y_max, color='red', s=50, zorder=5)
    plt.text(x_max, y_max + 0.5, f'{y_max}', fontsize=10, ha='center', va='bottom', color='red')

    plt.title(f"Streak Over Time{' - ' + str(year) if year else ''}", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Streak", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), fontsize=10)
    plt.tight_layout()

    # Save plot to BytesIO
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.getvalue()