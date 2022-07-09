##########################  Packages   #############################

import os
import sys
# import geopandas as geopd
import pandas as pd
from dotenv import load_dotenv as env
#-------------------------------------------------------------------#

env()   #Load variables from .env file
data = pd.read_csv(os.getenv('rain_data'), encoding='utf8') #Read csv file
data.drop(data.index[42:], inplace=True)  #Drop blank rows

##########################  Functions   #############################

def is_considered(row):
    nVals = nRecords = len(row) - 3
    for field in row:
        if not field:
            nVals -= 1
    #Fetch just records with 80 percent of data
    if nVals >= nRecords * 0.8:
        return True
#-------------------------------------------------------------------#

#Filter data
for i,n in data.notna().iterrows():
    if not is_considered(n):
        data.drop(index=i, inplace=True)
    data.fillna(0)

g = (sum(row[-1][4:]) for row in data.iterrows())