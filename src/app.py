import os, sys, io
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# import utils as utils
import scraper as scraper
from scraper import FundEntry
import datetime
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Flask, render_template, Response

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def index():
    return render_template("index.html", current_fund = scraper.get_entry(),
    change=scraper.fund_delta(),
    lin_tbl=stat_tbl(), log_tbl=stat_tbl(log="x"),
    dtbl=delta_tbl(),
    last_upd=scraper.last_entry_time(),status=scraper.scrape(checkstatus=True))

"""
plt figure to .png
"""
@app.route('/plot.png')
def plot_png():
    fig = scraper.render()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

"""
Table Generation
"""
# prediction stats table
def stat_tbl(log=""):
    next_check = scraper.time_to_check(log=log)
    end_miles = scraper.end_fund(log=log)
    model = "Log" if log else "Lin"
    out = f'''<table> <tr> <th>Select Checkpoint</th> <th>Est. Time to Next Check</th> </tr>
    <tr> <td>{next_check[0]}</td> <td>{next_check[1]}</td> </tr>
    <tr> <th>Est. End Fund ({model}Reg)</th> <th>All Milestones?</th> </tr>
    <tr> <td>{end_miles[0]}</td> <td>{end_miles[1]}</td> </tr>
    </table>'''
    return out

# daily changes table
def delta_tbl():
    out = "<table class='info-tbl'> <tr> <th>Day</th> <th>TK Increase</th> </tr>"
    out += f"<tr> <td>{1}</td> <td>{scraper.daily_delta(0)}</td> </tr>"
    day = 1
    while scraper.daily_delta(day) != 0 and day < scraper.DAYSPAN + 1:
        cur, prev = scraper.daily_delta(day), scraper.daily_delta(day - 1)
        percent = ((cur - prev) / prev) * 100 if prev != 0 else 0
        sign = "\u2191" if percent > 0 else "\u2193"
        if cur != 0:
            out += f"<tr> <td>{day+1}</td> <td>{cur} ({sign} {np.round(abs(percent), 3)}%)</td> </tr>"
        day += 1
    out += "</table>"
    return out

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)