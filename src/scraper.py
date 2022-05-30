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
OBSFILE = os.path.join(SAVE_DIR, "observed.txt")
SAVEFILE = os.path.join(SAVE_DIR, "fund.txt")
SAVE_NEW = os.path.join(SAVE_DIR, "fundv2.txt")

# fund specific
URL = "https://tankionline.com/pages/tanki-birthday-2022/" # when new fund website
CHECKPOINTS = [3] + list(range(6, 16))
REWARDS = ["Prot Slot", "Prot Slot", "Skin Cont", "Skin Cont", "Prot Slot", "Hyperion", "Blaster", "Armadillo", "Pulsar", "Crisis", "Surprise"]
START_DATE = pd.Timestamp("2022-05-27 2:00:00")
END_DATE = pd.Timestamp("2022-06-20 2:00:00")
DAYSPAN = int(mdates.date2num(END_DATE)) - int(mdates.date2num(START_DATE))


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

# archive stuff
def add_archives():
    archive_arr = np.array([])
    utils.save_entry(archive_arr, OBSFILE)

def add_entry():
    archive_arr = utils.load_entry(OBSFILE)
    # add 
    utils.save_entry(archive_arr, OBSFILE)

def check_archive():
    archive_arr = utils.load_entry(OBSFILE)
    print(archive_arr)
    return archive_arr

def to_csv():
    full_arr = utils.load_entry(SAVE_NEW)
    full_arr = full_arr.tolist()
    times, funds = [numd(dsnum(fund.time))-(START_DATE.to_pydatetime()).replace(tzinfo=datetime.timezone.utc) for fund in full_arr], [int(fund.value) for fund in full_arr]
    df = pd.DataFrame(np.transpose([times, funds]), columns=["Elapsed Time", "Fund"])
    df.to_csv(os.path.join(SAVE_DIR, "fund.csv"))

# reset fund data
# def reset():
#     utils.clean(SAVEFILE)
#     initialize_arr()

"""
Neater Utility Methods
"""
def dnum(date):
    return mdates.date2num(date)

def dsnum(dstr):
    return mdates.datestr2num(dstr)

def numd(num):
    return mdates.num2date(num)

def sn_num(num):
    return np.format_float_scientific(num, precision=3)

def entries():
    funds_arr = utils.load_entry(SAVE_NEW)
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
    funds_arr = utils.load_entry(SAVE_NEW)
    # prevent duplicates
    if fund_text in [fund.value for fund in funds_arr]:
        return fund_text
    funds_arr = np.append(funds_arr, FundEntry(fund_text))
    utils.save_entry(funds_arr, SAVE_NEW)
    return fund_text

def no_duplicates():
    funds_arr = utils.load_entry(SAVEFILE)
    archive_arr = utils.load_entry(OBSFILE)
    full_arr = np.concatenate((archive_arr, funds_arr))
    values = list(set([fund.value for fund in full_arr]))
    # print(np.sort(list(values)))
    no_dup = []
    for entry in full_arr:
        if entry.value in values:
            no_dup.append(entry)
            values.remove(entry.value)
    utils.save_entry(np.array(no_dup), SAVE_NEW)
    check = utils.load_entry(SAVE_NEW)
    print(check)

"""
Visualization
"""
# quick utility/helper methods
# get data
def get_data():
    # funds_arr = utils.load_entry(SAVEFILE)
    # archive_arr = utils.load_entry(OBSFILE)
    # full_arr = np.concatenate((archive_arr, treat_data(funds_arr))) if treat == True else np.concatenate((archive_arr, funds_arr))
    full_arr = utils.load_entry(SAVE_NEW)
    x, y = [fund.time for fund in full_arr], [(int(fund.value) / 1000000) for fund in full_arr]
    return x, y

fund_outages = [25, 26, 47, 48, 51, -1]
def treat_data(arr, indices=fund_outages):
    now = datetime.datetime.utcnow()
    num_samples = (now - START_DATE.to_pydatetime()).total_seconds() // (3*3600)
    arr = arr.tolist()
    out = []
    for i in indices:
        out.append(arr[i])
    for i in indices:
        arr.pop(i)
    return np.concatenate((np.array(out), np.random.choice(np.array(arr), int(num_samples), replace=False)))

def x_time(x):
    return dsnum(x)

# xlims
def get_xlim():
    today = datetime.datetime.utcnow().date()
    end_x = (today + datetime.timedelta(days=1))
    return pd.Timestamp(end_x)

# get checkpoint lines
def get_checklines(y):
    y_upper = 1.2 * max(y)
    for i in range(len(CHECKPOINTS)):
        if CHECKPOINTS[i] < max(y):
            plt.axhline(CHECKPOINTS[i], color='green', linestyle='--', alpha=0.35, label=f"Achieved: {REWARDS[i]}")
        elif CHECKPOINTS[i] < y_upper:
            plt.axhline(CHECKPOINTS[i], color='red', linestyle='--', alpha=0.35, label=f"Upcoming: {REWARDS[i]}")

def get_labels(m, b, log=''):
    x_exp = "log(x)" if log == "x" else "x"
    if m > 100:
        return f"y={(sn_num(m))}{x_exp}+{sn_num(m * dnum(START_DATE) + b)}"
    return f"y={np.round(m, 3)}{x_exp}+{np.round(m * dnum(START_DATE) + b, 3)}"

def regression(x, y, log=''):
    # logarithmic regression
    if 'x' in log:
        x = np.log(x) # y = mlog(x) + b
    if 'y' in log:
        y = np.log(y) # log(y) = mx + b; y = exp(mx + b)
    r = np.corrcoef(x, y)[0, 1]
    m = r * (np.std(y) / np.std(x))
    b = np.mean(y) - m * np.mean(x)
    print(m, b, x[0], y[0], m * x[0] + b, m * np.log(np.exp(x[0])+24) + b)
    return m, b

# scuffed :sob:
def visualize():
    x, y = get_data()
    x, y = np.sort(x), np.sort(y)
    x_time = dsnum(x)
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    plt.subplots_adjust(bottom=0.25)
    plt.plot(x_time, y, marker=".", linestyle='-', markersize=10)
    plt.title("Tanki Fund over Time", fontsize=20)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax.set_xlim(pd.Timestamp('2022-05-27 2:00:00'), get_xlim())
    plt.xticks(rotation=60)
    plt.xlabel("Time")
    ax.set_ylim(0, 1.2 * max(y))
    plt.ylabel("Fund (in millions)")
    get_checklines(y)
    lin_m, lin_b = regression(x_time, y)
    log_m, log_b = regression(x_time, y, log='x')
    xrange = [dsnum('2022-05-27 2:00:00'), dsnum(get_xlim().to_pydatetime().strftime('%Y-%m-%d %H:%M:%S'))]
    lin_xrange = np.linspace(xrange[0], 2 * xrange[1])
    plt.plot(lin_xrange, lin_m*lin_xrange+lin_b, color='black', linestyle="--", alpha=0.35, label=f"LinReg Prediction:\n{get_labels(lin_m, lin_b)}")
    plt.plot(lin_xrange, log_m*(np.log(lin_xrange)) + log_b, color='orange', linestyle="--", alpha=0.4, label=f"LogReg Prediction\n{get_labels(log_m, log_b, log='x')}")
    print(log_m*(np.log(xrange[0]))+log_b, log_m*(np.log(xrange[1]))+log_b)
    plt.legend(loc=2, fontsize=8)
    return fig

"""
Change in Fund Values over time
"""

def fund_delta():
    funds_arr = utils.load_entry(SAVE_NEW)
    if len(funds_arr) > 1:
        return int(funds_arr[-1].value) - int(funds_arr[-2].value)
    else:
        return 0

# daily delta stuff
def nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

# check if the fund entry is within 1 day pm 30 min of the start date
def one_day_delta(fund, start, epsilon=36/864): # 5 min epsilon
    return (dsnum(fund.time) - start) <= 1 + (2 * epsilon) and (dsnum(fund.time) - start) >= 1 - (2 * epsilon)

# daily change
def daily_delta(day=0):
    if day < 0 or day > DAYSPAN:
        return 0
    funds_arr = utils.load_entry(SAVE_NEW)
    dstart = dnum(START_DATE) + day
    start_filtered, end_filtered = [fund for fund in funds_arr if one_day_delta(fund, dstart - 1)] or [FundEntry(0)], [fund for fund in funds_arr if one_day_delta(fund, dstart)] or [FundEntry(0)]
    print(end_filtered)
    start_times, end_times = [dsnum(fund.time) for fund in start_filtered], [dsnum(fund.time) for fund in end_filtered]
    start_idx = nearest_index(start_times, dstart)
    end_idx = nearest_index(end_times, dstart + 1)
    start_val, end_val = start_filtered[start_idx].value, end_filtered[end_idx].value
    if end_val != 0:
        return int(end_val) - int(start_val)
    else:
        return 0

def get_index_from_check(y):
    try:
        c_next = [c for c in CHECKPOINTS if c > y][0]
    except IndexError:
        c_next = CHECKPOINTS[-1]
    idx = CHECKPOINTS.index(c_next)
    return idx

def time_to_check(log='', index=None):
    x, y = get_data()
    x_time = dsnum(x)
    m, b = regression(x_time, y, log)
    end = END_DATE.to_pydatetime().replace(tzinfo=datetime.timezone.utc)
    idx = get_index_from_check(max(y)) if not index else index
    c_next = CHECKPOINTS[idx]
    eqn = (c_next - b) / m
    x_next = numd(np.exp(eqn)) if log == 'x' else numd(eqn)
    x_next = x_next.replace(tzinfo=datetime.timezone.utc)
    if (end - x_next).total_seconds() > 0:
        t_next = tdelta_format(x_next - datetime.datetime.now(datetime.timezone.utc))
        return REWARDS[idx], f"{t_next} ({x_next.strftime('%m-%d %H:%M')})"
    return REWARDS[idx], "Cannot Reach"

def end_fund(log=""):
    x, y = get_data()
    x_time = dsnum(x)
    m, b = regression(x_time, y, log=log)
    end = np.log(dnum(END_DATE)) if log =="x" else dnum(END_DATE)
    y_final = np.round(m * end + b, 3)
    if y_final < CHECKPOINTS[-1]:
        idx = get_index_from_check(y_final)
        return f"{y_final}M Tankoins", f"No (Will miss {REWARDS[idx]})"
    return f"{y_final}M Tankoins", 'Yes'
    # print(mdates.date2num(START_DATE), mdates.date2num(END_DATE))
    

def tdelta_format(td):
    seconds = np.round(td.total_seconds())
    days, rem1 = divmod(seconds, 86400)
    hours, rem2 = divmod(rem1, 3600)
    minutes, seconds = divmod(rem2, 60)
    if days > 0:
        return f"{int(days)}d {int(hours)}h {int(minutes)}m"
    return f"{int(hours)}h {int(minutes)}m"