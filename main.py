from algorithm import bshalgorithm
from streakIdentifier import streakIdentifier
from advice import give_advice_text
# from dailyReturns import daily_returns
from plotCharts import generate_sma_chart
from streakChart import generate_streak_chart
from start import SMA
import pandas as pd
from flask import Flask, render_template, Response, request

app = Flask(__name__)

def load_prices(ticker="MSFT"):  
    df = pd.read_csv(f"{ticker}.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    for col in ["Close/Last", "High", "Low"]:
        df[col] = df[col].astype(str).str.lstrip("$").astype(float)
    # Computing SMA 20 and 50 to update dataframe
    df['SMA'] = SMA(df['Close/Last'], 20)
    df['SMA1'] = SMA(df['Close/Last'], 50)
    return df

@app.route("/", methods=["GET", "POST"])   
def home():
    advice_output = ""   
    
    if request.method == "POST":   
        ticker = request.form.get("ticker", "MSFT")
        strategy = request.form.get("strategy", "default")
        # Load prices & run algorithm
        df = load_prices(ticker)
        # Computing streak to update dataframe
        sdf = streakIdentifier(df)
        # Computing algorithm signals to update dataframe
        fdata, maxprofit = bshalgorithm(sdf)
        # Generate advice
        advice_output = give_advice_text(fdata)
        fdata.to_csv('ndata.csv', index=False)
    return render_template("index.html", advice=advice_output)  

# Route to generate SMA chart as PNG image
@app.route("/plot.png")
def plot_png():
    # Get the company ticker from URL parameters, default to "MSFT" if not provided
    ticker = request.args.get("ticker", "MSFT")  
    
    # Get the SMA window size from URL parameters, default to 20 if not provided or invalid
    try:
        window_size = int(request.args.get("t", 20))
    except (ValueError, TypeError):
        window_size = 20

    # Generate the SMA chart as PNG bytes using the selected ticker and window size
    png_bytes = generate_sma_chart(window_size, ticker)
    
    # Return the PNG image as a response with proper MIME type
    return Response(png_bytes, mimetype="image/png")


# Route to generate Streak chart as PNG image
@app.route("/streak.png")
def streak_png():
    # Get the company ticker from URL parameters, default to "MSFT" if not provided
    ticker = request.args.get("ticker", "MSFT")
    
    # Get the year to filter streaks, default to 2020 if not provided
    year = request.args.get("year", "2020")
    
    # Load price data for the selected company
    df = load_prices(ticker)
    
    # Generate streak chart for the selected ticker and year as PNG bytes
    png_bytes = generate_streak_chart(df, year, ticker)
    
    # Return the PNG image as a response with proper MIME type
    return Response(png_bytes, mimetype="image/png")


@app.route('/graph')
def graph():
    return render_template("graph.html")

@app.route('/smagraph')
def smagraph():
    return render_template("frontend.html")

if __name__ == "__main__":
    app.run(debug=True)
