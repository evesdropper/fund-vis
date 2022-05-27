 # necessary imports - scraping
import requests
from bs4 import BeautifulSoup
import pickle

# data analysis
import datetime
import numpy as np
# import cvxpy as cp - used for LPs but we don't have any now
import matplotlib.pyplot as plt

# utility - store fund entries
class FundEntry():
    
    def __init__(self, value):
        self.time = datetime.datetime.utcnow().strftime('%m-%d %H-%M-%S')
        self.value = value    
    
    def __repr__(self):
        return f"{self.time}: {self.value}"
    
    def __str__(self):
        return f"Fund at {self.time}: {self.value}"