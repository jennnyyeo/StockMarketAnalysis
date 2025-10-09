import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from smaFunc import SMA

# Default CSV file and label interval
CSV_FILE = "MSFT.csv"
# Show labels on every 50th data point for readability
LABEL_EVERY = 50

def generate_sma_chart(window_size=20, ticker="MSFT"):
    if window_size not in [20, 50]:
        window_size = 20

    # Load CSV for the selected ticker
    # dynamically load CSV based on ticker
    df = pd.read_csv(f"{ticker}.csv")  
    # convert Date column to datetime 
    df['Date'] = pd.to_datetime(df['Date'])
    # Clean Close/Last column: remove $ and convert to float
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)

    # Compute SMA for the selected window
    sma_col = f'SMA_{window_size}'
    # add SMA to dataframe
    df[sma_col] = SMA(df['Close/Last'], window_size)

    # Create plot
    plt.figure(figsize=(12,6))
    # Plot close prices
    plt.plot(df['Date'], df['Close/Last'], linewidth=1, label=f'{ticker} Close Price')
    # Plot SMA line
    plt.plot(df['Date'], df[sma_col], linestyle='--', linewidth=1.5, color='orange', label=f'{window_size}-Day SMA')

    # Add SMA value labels at intervals for readability
    for idx in df[sma_col].iloc[::LABEL_EVERY].index:
        y = df[sma_col].iloc[idx]
        # skip None/NaN values
        if pd.notna(y):
            x = df['Date'].iloc[idx]
            # adjust y offset to prevent overlap
            plt.text(x, y+30, f'{y:.1f}', fontsize=8, ha='center', va='bottom')

    # Chart title and labels
    plt.title(f"{ticker} Close Price vs {window_size}-Day SMA", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Stock Price (USD)", fontsize=12)
    # rotate x-axis labels for readability
    plt.xticks(rotation=45)
    # light grid lines
    plt.grid(True, linestyle='--', alpha=0.5)
    # Legend outside the plot
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), fontsize=10)
    plt.tight_layout()

    # Save figure to bytes buffer
    buf = io.BytesIO()
    # save as PNG
    plt.savefig(buf, format='png')
    # close plot to free memory
    plt.close()
    # move buffer pointer to beginning
    buf.seek(0)
    # return PNG image bytes
    return buf.getvalue()