from flask import Flask, Response, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import os

app = Flask(__name__)

CSV_FILE = "MSFT.csv"   
LABEL_EVERY = 50        

@app.route("/")
def dashboard():
    return render_template("frontend.html")

@app.route("/plot.png")
def plot_png():
    try:
        window_size = int(request.args.get("t", 20))
        if window_size <= 0:
            window_size = 20
    except ValueError:
        window_size = 20

    if not os.path.exists(CSV_FILE):
        return Response("CSV file not found.", mimetype="text/plain")

    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)

    sma_col = f'SMA_{window_size}'
    df[sma_col] = df['Close/Last'].rolling(window=window_size).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close/Last'], linewidth=1, label='MSFT Close Price')
    plt.plot(df['Date'], df[sma_col], linestyle='--', linewidth=1.5, color='orange', label=f'{window_size}-Day SMA')

    for idx in df[sma_col].iloc[::LABEL_EVERY].index:
        y = df[sma_col].iloc[idx]
        if pd.notna(y):
            x = df['Date'].iloc[idx]
            plt.text(x, y + 20, f'{y:.1f}', fontsize=8, ha='center', va='bottom')

    plt.title(f"MSFT Close Price vs {window_size}-Day SMA", fontsize=14)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Stock Price (USD)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)