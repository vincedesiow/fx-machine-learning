import pandas as pd
import os

store = pd.HDFStore('data.hdf5')

temp = []

# select all csv files in folder
# run file in data folder
for file in os.listdir("stock_indices_raw"):
	if file.endswith(".csv"):
		ind = pd.read_csv("stock_indices_raw\\"+file)
		ind.index = pd.to_datetime(ind.Date, format="%Y/%m/%d")
		ind = ind.drop("Date", axis=1)
		ind = ind.add_prefix(os.path.splitext(file)[0] + '_')
		temp.append(ind)
store["indices"] = pd.concat(temp, axis=1)