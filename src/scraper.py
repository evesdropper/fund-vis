 # necessary imports - scraping and heroku being retarded
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import utils as utils
import requests
from bs4 import BeautifulSoup

# data analysis
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# big capital letters
CWD = os.getcwd()
# DOCS = os.environ["DOCS"]
# PROJ_DIR = os.path.join(DOCS, "tonk/fund-vis/src")
SAVE_DIR = os.path.join(CWD, "saved")
SAVEFILE = os.path.join(SAVE_DIR, "fund.txt")

# fund specific
URL = "https://tankionline.com/pages/tanki-birthday-2022/" # when new fund website
CHECKPOINTS = [3] + list(range(6, 16))
REWARDS = ["Prot Slot", "Prot Slot", "Skin Cont", "Skin Cont", "Prot Slot", "Hyperion", "Blaster", "Armadillo", "Pulsar", "Crisis", "Surprise"]
START_DATE = pd.Timestamp("2022-05-27 2:00:00")
END_DATE = pd.Timestamp("2022-06-20 2:00:00")

"""
Base Setup
"""
# fund entries
class FundEntry():
    
    def __init__(self, value, time=None):
        self.time = datetime.datetime.utcnow().strftime('%m-%d %H:%M') if not time else time.strftime('%m-%d %H:%M')
        self.value = value
    
    def __repr__(self):
        return f"{self.time}: {self.value}"
    
    def __str__(self):
        return f"Fund at {self.time}: {self.value}"

# start a new fund array
def initialize_arr():
    funds_arr = np.array([])
    utils.save_entry(funds_arr, SAVEFILE)

def delerror():
    funds_arr = utils.load_entry(SAVEFILE)
    funds_arr = funds_arr[:-1]
    utils.save_entry(funds_arr, SAVEFILE)

def delallerrors():
    funds_arr = utils.load_entry(SAVEFILE)
    funds_arr = funds_arr.tolist()
    funds_arr = [fund for fund in funds_arr if fund.value != 0]
    funds_arr = np.array(funds_arr)
    utils.save_entry(funds_arr, SAVEFILE) 

# reset fund data
def reset():
    utils.clean(SAVEFILE)
    initialize_arr()

"""
Major Workflow
"""
def scrape(checkstatus=False):
    try: 
        page = requests.get(URL, timeout=(5, 15))
        soup = BeautifulSoup(page.content, "html.parser")
        fund = soup.find_all("span", class_="ms-3")
        fund_text = fund[0].text
        if checkstatus:
            return "Up to date"
    except:
        if checkstatus:
            return "Site is down; using backups."
        fund_text = last_entry()
    return fund_text

# fund 
def get_entry():
    fund_text = scrape()
    funds_arr = utils.load_entry(SAVEFILE)
    funds_arr = np.append(funds_arr, FundEntry(fund_text))
    utils.save_entry(funds_arr, SAVEFILE)
    return fund_text


"""
Visualization
"""
# get data
def get_data():
    funds_arr = utils.load_entry(SAVEFILE)
    x, y = [fund.time for fund in funds_arr], [(int(fund.value) / 1000000) for fund in funds_arr]
    return x, y

def x_time(x):
    return mdates.datestr2num(x)

# xlims
def get_xlim():
    today = datetime.datetime.utcnow().date()
    end_x = (today + datetime.timedelta(days=1))
    return pd.Timestamp(end_x)

def regression(x, y, log=''):
    # logarithmic regression
    if 'x' in log:
        x = np.log(x) # y = mlog(x) + b
    if 'y' in log:
        y = np.log(y) # log(y) = mx + b; y = exp(mx + b)
    r = np.corrcoef(x, y)[0, 1]
    # print(r,r**2)
    m = r * (np.std(y) / np.std(x))
    b = np.mean(y) - m * np.mean(x)
    # print(m, b, x[0], x[0]+ 24, y[0], y[-1])
    # print(m * x[0] + b, m * x[-1] + b, m * np.log(np.exp(x[0]) + 24) + b)
    return m, b

def next_checkpoint(log=''):
    x, y = get_data()
    x_time = mdates.datestr2num(x)
    m, b = regression(x_time, y, log)
    c_next = [c for c in CHECKPOINTS if c > max(y)][0]
    idx = CHECKPOINTS.index(c_next)
    eqn = (c_next - b) / m
    x_next = mdates.num2date(np.exp(eqn)) if log == 'x' else mdates.num2date(eqn)
    x_next = x_next.replace(tzinfo=datetime.timezone.utc)
    t_next = tdelta_format(x_next - datetime.datetime.now(datetime.timezone.utc))
    return REWARDS[idx], f"{t_next} ({x_next.strftime('%m-%d %H:%M')})"

def end_fund(log=""):
    x, y = get_data()
    x_time = mdates.datestr2num(x)
    m, b = regression(x_time, y, log=log)
    end = np.log(mdates.date2num(END_DATE)) if log =="x" else mdates.date2num(END_DATE)
    y_final = m * end + b
    # print(mdates.date2num(START_DATE), mdates.date2num(END_DATE))
    return f"{np.round(y_final, 3)}M Tankoins", "Yes" if y_final > CHECKPOINTS[-1] else "No"

def tdelta_format(td):
    seconds = np.round(td.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m"


# scuffed :sob:
def visualize():
    x, y = get_data()
    x_time = mdates.datestr2num(x)
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    plt.subplots_adjust(bottom=0.25)
    plt.plot(x_time, y, marker=".", linestyle='-', markersize=10)
    plt.title("Tanki Fund over Time", fontsize=20)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax.set_xlim(pd.Timestamp('2022-05-27 2:00:00'), get_xlim())
    plt.xticks(rotation=60)
    plt.xlabel("Time")
    y_upper = 1.2 * max(y)
    ax.set_ylim(0, y_upper)
    # checkpoint lines
    for i in range(len(CHECKPOINTS)):
        if CHECKPOINTS[i] < max(y):
            plt.axhline(CHECKPOINTS[i], color='green', linestyle='--', alpha=0.35, label=f"Achieved: {REWARDS[i]}")
        elif CHECKPOINTS[i] < y_upper:
            plt.axhline(CHECKPOINTS[i], color='red', linestyle='--', alpha=0.35, label=f"Upcoming: {REWARDS[i]}")
    plt.ylabel("Fund (in millions)")
    lin_m, lin_b = regression(x_time, y)
    log_m, log_b = regression(x_time, y, log='x')
    xrange = [mdates.datestr2num('2022-05-27 2:00:00'), mdates.datestr2num(get_xlim().to_pydatetime().strftime('%Y-%m-%d %H:%M:%S'))]
    lin_xrange = np.linspace(xrange[0], 2 * xrange[1])
    # log_yrange = np.linspace(0, 15)
    plt.plot(lin_xrange, lin_m*lin_xrange+lin_b, color='black', linestyle="--", alpha=0.35, label=f"LinReg Prediction:\ny={np.round(lin_m, 3)}x+{np.round(lin_m * mdates.date2num(START_DATE) + lin_b, 3)}")
    plt.plot(lin_xrange, log_m*(np.log(lin_xrange)) + log_b, color='green', linestyle="--", alpha=0.35, label=f"LogReg Prediction\ny={np.format_float_scientific(log_m, precision=3)}log(x)+{np.format_float_scientific(log_m * mdates.date2num(START_DATE) + log_b, precision=3)}")
    plt.legend(loc=2, fontsize=8)
    return fig

"""
Utility Functions
"""
def entries():
    funds_arr = utils.load_entry(SAVEFILE)
    return funds_arr

def last_entry():
    return entries()[-1].value

def last_entry_time():
    return entries()[-1].time

def showplot():
    visualize()
    plt.show()

def render():
    get_entry()
    out = visualize()
    return out

"""
Change in Fund Values over time
"""

def fund_delta():
    funds_arr = utils.load_entry(SAVEFILE)
    if len(funds_arr) > 1:
        return int(funds_arr[-1].value) - int(funds_arr[-2].value)
    else:
        return 0

# daily delta stuff
def nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

# check if the fund entry is within 1 day of the start date
def one_day_delta(fund, start, epsilon=3/864): # 5 min epsilon
    return (mdates.datestr2num(fund.time) - start) <= (1 + epsilon) and (mdates.datestr2num(fund.time) - start) >= 1 - (3.5 * epsilon)

# daily change
def daily_delta(day=0):
    if day < 0 or day > int(mdates.date2num(END_DATE)) - int(mdates.date2num(START_DATE)):
        return 0
    funds_arr = utils.load_entry(SAVEFILE)
    dstart = mdates.date2num(START_DATE) + day
    start_filtered, end_filtered = [fund for fund in funds_arr if one_day_delta(fund, dstart - 1)] or [FundEntry(0)], [fund for fund in funds_arr if one_day_delta(fund, dstart)] or [FundEntry(0)]
    start_times, end_times = [mdates.datestr2num(fund.time) for fund in start_filtered], [mdates.datestr2num(fund.time) for fund in end_filtered]
    start_idx = nearest_index(start_times, dstart)
    end_idx = nearest_index(end_times, dstart + 1)
    start_val, end_val = start_filtered[start_idx].value, end_filtered[end_idx].value
    if end_val != 0:
        return int(end_val) - int(start_val) # f"<tr> <td>{day+1}</td> <td>{int(end_val) - int(start_val)}</td> </tr>"
    else:
        return 0

def delta_tbl():
    out = "<table class='info-tbl'> <tr> <th>Day</th> <th>TK Increase</th> </tr>"
    out += f"<tr> <td>{1}</td> <td>{daily_delta(0)}</td> </tr>"
    for day in range(1, int(mdates.date2num(END_DATE)) - int(mdates.date2num(START_DATE)) + 1):
        cur, prev = daily_delta(day), daily_delta(day - 1)
        percent = ((cur - prev) / prev) * 100 if prev != 0 else 0
        sign = "\u2191" if percent > 0 else "\u2193"
        if cur != 0:
            out += f"<tr> <td>{day+1}</td> <td>{cur} ({sign} {np.round(abs(percent), 3)}%)</td> </tr>"
    out += "</table>"
    # print(out)
    return out