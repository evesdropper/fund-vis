import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import scraper as scraper
from scraper import FundEntry
import io
import datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", current_fund = scraper.get_entry(), last_upd=datetime.datetime.now().strftime("%m-%d %H:%M"))

@app.route('/plot.png')
def plot_png():
    fig = scraper.visualize()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)