import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Select SMA window size at runtime
# -----------------------------
window_size = int(input("Enter SMA window size (e.g., 10, 20, 30, 40, 50): "))

# Load CSV
df = pd.read_csv("MSFT.csv")

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Remove $ and convert Close price to float
df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)

# Compute SMA
df[f'SMA_{window_size}'] = df['Close/Last'].rolling(window=window_size).mean()

# Plot
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close/Last'], linewidth=0.5, label='MSFT Close Price')
plt.plot(df['Date'], df[f'SMA_{window_size}'], linestyle='--', linewidth=0.5, color='orange',
         label=f'MSFT SMA {window_size} Days')

# Label SMA values every 20 points using slicing
every20 = df[f'SMA_{window_size}'].iloc[::50]  # every 20th point
for idx in every20.index:
    y = df[f'SMA_{window_size}'].iloc[idx]
    if pd.notna(y):
        x = df['Date'].iloc[idx]
        plt.text(x, y + 40, f'{y:.1f}', fontsize=8, ha='center', va='bottom')


# Customize chart
plt.title(f"MSFT Close Price vs {window_size}-Day SMA")
plt.xlabel("Date")
plt.ylabel("Stock Price (USD)")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(
    loc='upper left',
    bbox_to_anchor=(1, 1),
    labelspacing=0.5,
    fontsize=10
)
plt.tight_layout()
plt.show()
