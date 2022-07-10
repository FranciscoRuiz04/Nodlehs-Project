##########################  Packages   #############################

import os
import sys
import geopandas as geopd
import matplotlib.pyplot as plt
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
    #Fetch just records with 80 percent of data or major
    if nVals >= nRecords * 0.8:
        return True
#-------------------------------------------------------------------#

#Filter data
for i,n in data.notna().iterrows():
    if not is_considered(n):
        data.drop(index=i, inplace=True)
    data.fillna(0)

#Generate a tuple with the total sum
# instead of periodical records
totalP = (row[2:5] + (sum(row[5:]),) for row in data.itertuples())

heads = list(data.columns[1:4]) #Colnames without ID field
heads.append("Total")
#Create an enmpty outcome dataframe
geoData = pd.DataFrame(columns=heads)

#Fill geoData
for i,rec in enumerate(totalP):
    geoData.loc[i] = rec

geo = geopd.read_file(os.getenv('myshp'))
geoData = geo.merge(geoData, on='Nombre')

if __name__ == '__main__':
    # geoData.plot()
    # plt.show()
    print(geo.crs)