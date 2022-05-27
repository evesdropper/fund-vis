 # necessary imports - scraping
import os
import requests
from bs4 import BeautifulSoup

# data analysis
import datetime
import numpy as np
import matplotlib.pyplot as plt

# big capital letters
CWD = os.getcwd()
SAVE_DIR = os.path.join(CWD, "saved")

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


def get_entry():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    fund = soup.find_all("span", class_="ms-3")
    return fund[0].text