from flask import Flask, Response, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__)

# -----------------------------
# Configuration
# -----------------------------
WINDOW_SIZE = 20        # Default SMA window size
CSV_FILE = "MSFT.csv"   # Path to CSV file
LABEL_EVERY = 50        # Show SMA labels every N points

# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def dashboard():
    """Render the main dashboard page from templates folder."""
    return render_template("frontend.html")  # Flask looks inside templates automatically

@app.route("/plot.png")
def plot_png():
    """Generate and return the MSFT SMA chart as a PNG image."""
    if not os.path.exists(CSV_FILE):
        return Response("CSV file not found.", mimetype="text/plain")

    # Load and process data
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)

    # Compute SMA
    sma_col = f'SMA_{WINDOW_SIZE}'
    df[sma_col] = df['Close/Last'].rolling(window=WINDOW_SIZE).mean()

    # Create plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close/Last'], linewidth=1, label='MSFT Close Price')
    plt.plot(df['Date'], df[sma_col], linestyle='--', linewidth=1.5, color='orange',
             label=f'{WINDOW_SIZE}-Day SMA')

    # Add SMA labels every LABEL_EVERY points
    for idx in df[sma_col].iloc[::LABEL_EVERY].index:
        y = df[sma_col].iloc[idx]
        if pd.notna(y):
            x = df['Date'].iloc[idx]
            plt.text(x, y + 20, f'{y:.1f}', fontsize=8, ha='center', va='bottom')

    # Customize chart
    plt.title(f"MSFT Close Price vs {WINDOW_SIZE}-Day SMA", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Stock Price (USD)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
    plt.tight_layout()

    # Save plot to BytesIO buffer and return as PNG response
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
