# necessary imports
import time, datetime
import asyncio
import pickle
import numpy as np
import pandas as pd

# selenium imports
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.common.by import By

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome('C:/Program Files (x86)/chromedriver.exe',options=option)

"""
Setup: Main Variables
"""
TIMES = np.array([1, 2, 3])
FUNDS = np.array([4, 5, 6]) # array of funds
DATASET = pd.DataFrame({'Time': [TIMES], 'Fund': [FUNDS]})
INTERVAL = 9000 # interval between each check in seconds
URL = "https://tankionline.com/pages/tanki-sport-season4/?lang=en" # change to current fund
CLASS_NAME = "prize-fond" # class name, bruh use id smh
np.save("times.npy", TIMES)
np.save("funds.npy", FUNDS)
TIMES_DATA = "times.npy"
FUNDS_DATA = "funds.npy"

"""
Get Data
"""

def get_data():
    time_data, fund_data = np.load(TIMES_DATA), np.load(FUNDS_DATA)
    driver.get(URL)
    data = driver.find_element(By.CLASS_NAME, CLASS_NAME)
    fund_data = np.append(FUNDS, int(data.text.replace(" ", "")) / 1000)
    update_time_raw = datetime.datetime.utcnow()
    update_time = update_time_raw.strftime("%Y-%m-%d %H:%M:%S")
    time_data = np.append(TIMES, update_time)
    np.save(TIMES_DATA, time_data)
    np.save(FUNDS_DATA, fund_data)
    print("Done")

def display_df():
    df = pd.DataFrame({'Time': np.load(TIMES_DATA), 'Fund': np.load(FUNDS_DATA)})
    print(df)

def main():
    pass