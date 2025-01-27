import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from os import path, listdir 
from matplotlib.backends.backend_pdf import PdfPages

file = "/home/user293/Documents/selections/python/Outputs/TrackSelection/LambdacCompIPAll.csv"

basedir=f"{file}/.."
sys.path.insert(0,basedir)

# Load the CSV file
csv_file = file  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

MinPT = df["MinPT"]
MinP = df["MinP"]
MinIPChi2 = df["MinIPChi2"]

efficiency = df["#XiLambda"]
purity = (df["#XiLambda"] * 504) / (df["#Lambda"] * 464)
