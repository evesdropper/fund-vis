 # necessary imports - scraping
import os, utils
import requests
from bs4 import BeautifulSoup

# data analysis
import datetime
import numpy as np
import matplotlib.pyplot as plt

# big capital letters
CWD = os.getcwd()
SAVE_DIR = os.path.join(CWD, "saved")
SAVEFILE = os.path.join(SAVE_DIR, "fund.txt")

URL = "https://tankionline.com/pages/tanki-birthday-2022/" # when new fund website

# fund entries
class FundEntry():
    
    def __init__(self, value):
        self.time = datetime.datetime.utcnow().strftime('%m-%d %H-%M-%S')
        self.value = value    
    
    def __repr__(self):
        return f"{self.time}: {self.value}"
    
    def __str__(self):
        return f"Fund at {self.time}: {self.value}"

# start a new fund array
def initialize_arr():
    funds_arr = np.array([])
    utils.save_entry(funds_arr, SAVEFILE)

# reset fund data
def reset():
    utils.clean_dirs(SAVE_DIR)
    initialize_arr()

def get_entry():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    fund = soup.find_all("span", class_="ms-3")
    funds_arr = utils.load_entry(SAVEFILE)
    funds_arr = np.append(funds_arr, FundEntry(fund[0].text))
    utils.save_entry(funds_arr, SAVEFILE)
    return fund[0].text, funds_arr


