# necessary imports
import time, datetime
import requests, json
import numpy as np
import pandas as pd

"""
Setup: Main Variables
"""
FUNDS = np.array([]) # array of funds
INTERVAL = 9000 # interval between each check in seconds

"""
Get Data
"""