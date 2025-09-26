from flask import Flask, Response, render_template, request
import pandas as pd
import io
import os
import matplotlib
matplotlib.use('Agg')   # Fixes the Tkinter backend issue
import matplotlib.pyplot as plt


app = Flask(__name__)

CSV_FILE = "MSFT.csv"   
LABEL_EVERY = 50        

@app.route("/")
def dashboard():
    return render_template("frontend.html")

@app.route("/plot.png")
def plot_png():
    # Only allow 20 or 50
    try:
        window_size = int(request.args.get("t", 20))
        if window_size not in [20, 50]:
            window_size = 20  # default to 20 if invalid
    except (ValueError, TypeError):
        window_size = 20

    if not os.path.exists(CSV_FILE):
        return Response("CSV file not found.", mimetype="text/plain")

    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)

    # KAI JUN'S CODE
    def SMA(close, period):
        sma = []
        for i in range(len(close)):
            if i < period - 1:
                sma.append(None)
            else:
                total = 0
                for j in range(period):
                    total+=close[i-j] 
                sma.append(total / period)
        return sma
    
    sma_col = f'custom_SMA_{window_size}'
    df[sma_col] = SMA(df['Close/Last'], window_size)

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close/Last'], linewidth=1, label='MSFT Close Price')
    plt.plot(df['Date'], df[sma_col], linestyle='--', linewidth=1.5, color='orange',
             label=f'{window_size}-Day SMA')

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