from algorithm import bshalgorithm
from streakIdentifier import streakIdentifier
from advice import give_advice_text
# from dailyReturns import daily_returns
from plotCharts import generate_sma_chart
from streakChart import generate_streak_chart
import pandas as pd
from flask import Flask, render_template, Response, request 

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

@app.route("/plot.png")
def plot_png():
    # Get SMA window from URL param, default to 20
    try:
        window_size = int(request.args.get("t", 20))
    except (ValueError, TypeError):
        window_size = 20

    png_bytes = generate_sma_chart(window_size)
    return Response(png_bytes, mimetype="image/png")

@app.route("/streak.png")
def streak_png():
    year = request.args.get("year", "All")  # default: all years
    png_bytes = generate_streak_chart(year)
    return Response(png_bytes, mimetype="image/png")

@app.route('/graph')
def graph():
    return render_template("graph.html")

@app.route('/smagraph')
def smagraph():
    return render_template("frontend.html")

if __name__ == "__main__":
    app.run(debug=True)
