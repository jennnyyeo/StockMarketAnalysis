from algorithm import bshalgorithm
from streakIdentifier import streakIdentifier
from advice import give_advice_text
from dailyReturns import daily_returns
from plotCharts import generate_sma_chart
from streakChart import generate_streak_chart
from smaFunc import SMA
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

def load_priceDR(ticker='MSFT'):
    data = pd.read_csv(f"{ticker}.csv")

    return data


def table_build(data, cols):
    df = data[cols].copy()
    classes = pd.DataFrame('', index=df.index, columns=df.columns)

    for col in [c for c in ['Signal'] if c in df.columns]:
        classes[col] = (
            df[col].astype(str).str.strip().str.lower().map(
                {'buy': 'cell-buy', 'sell': 'cell-sell'}).fillna('')
        )

    styler = (
        df.style.set_table_attributes(
                'class="table table-sm table-striped table-hover table-bordered mb-0 text-nowrap table-centered text-center"'
            )
            .set_td_classes(classes)
    )
    
    table_html = styler.to_html()

    return table_html


@app.route("/", methods=["GET", "POST"])
def home():
    advice_output = ""
    table_html = None
    maxprofit = None

    if request.method == "POST":
        ticker = request.form.get("ticker", "MSFT")
        strategy = request.form.get("strategy", "default")

        # Load prices & run algorithm
        df = load_prices(ticker)

        # Computing streak to update dataframe
        sdf = streakIdentifier(df)

        # Computing algorithm signals to update dataframe
        fdata, maxprofit = bshalgorithm(sdf)

        drdf = load_priceDR(ticker)
        dailyreturns = daily_returns(drdf)
        fdata['Daily Return (%)'] = dailyreturns['Daily Return (%)']

        # Generate advice
        advice_output = give_advice_text(fdata)

        desired_cols = ['Date', 'Close/Last',
                        'SMA', 'SMA1', 'StreakIdx', 'Signal', 'Daily Return (%)']

        fdata['Date'] = pd.to_datetime(
            fdata['Date'], errors='coerce').dt.strftime("%Y/%m/%d")

        try:
            if desired_cols:
                table_html = table_build(fdata, desired_cols)
        except Exception as e:
            advice_output = f'Could not build table: {e}\nColumns in fdata: {list(fdata.columns)}'

        fdata.to_csv('ndata.csv', index=False)
    return render_template("index.html", advice=advice_output, table_html=table_html, maxprofit=maxprofit)

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
