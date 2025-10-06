from start import SMA
from algorithm import bshalgorithm
from streakIdentifier import streakIdentifier
from advice import give_advice_text
# from dailyReturns import daily_returns
# from plotCharts import plot_png
import pandas as pd
from flask import Flask, render_template, request  

app = Flask(__name__)

def load_prices(ticker="MSFT"):  
    df = pd.read_csv(f"{ticker}.csv")
    for col in ["Close/Last", "High", "Low"]:
        df[col] = df[col].astype(str).str.lstrip("$").astype(float)
    return df

@app.route("/", methods=["GET", "POST"])   
def home():
    advice_output = ""   
    
    if request.method == "POST":   
        ticker = request.form.get("ticker", "MSFT")
        strategy = request.form.get("strategy", "default")
        
        # Load prices & run algorithm
        df = load_prices(ticker)
        ndata, buy_dates, sell_dates = bshalgorithm(df)

        # Generate advice
        advice_output = give_advice_text(ndata)

    return render_template("index.html", advice=advice_output)  

if __name__ == "__main__":
    app.run(debug=True)
