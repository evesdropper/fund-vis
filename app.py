import src.scraper as scraper
import src.fund as fund
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/plot.png')
def plot_png():
    fig = scraper.visualize()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)