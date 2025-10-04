from start import SMA
from algorithm import bshalgorithm
from streakIdentifier import streakIdentifier
# from dailyReturns import daily_returns
# from plotCharts import plot_png
import pandas as pd
from flask import Flask, Response, render_template, request

app = Flask(__name__)

def load_prices():
    df = pd.read_csv("MSFT.csv")
    df["Close/Last"] = df["Close/Last"].astype(str).str.lstrip("$").astype(float)
    

results_cache = None

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
    df = pd.read_csv('MSFT.csv')
    for col in ['Close/Last', 'High', 'Low']:
        df[col] = df[col].str.replace('$', '').astype(float)

    ndata, buy_dates, sell_dates = bshalgorithm(df)