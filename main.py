# from start import SMA
# from algorithm import bshalgorithm
# from dailyReturns import daily_returns
# from plotCharts import plot_png
from flask import Flask, Response, render_template, request

app = Flask(__name__)

results_cache = None

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)