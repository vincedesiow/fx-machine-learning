import h5py
import pandas as pd
import numpy as np
import quandl
import datetime

# create data.hdf5 file in current working directory (uncomment the code below if file has not been created)
# data = h5py.File('data.hdf5', 'w')

# access and write data.hdf5 file using pandas.DataFrame.HDFStore
store = pd.HDFStore('data.hdf5')

# key in your quandl authtoken
# quandl.ApiConfig.api_key = <your_token>

# start & end dates for downloading data
start = "2007-07-01"
end = "2017-06-30"

# fx historical data (daily - 24/7)
temp = [] # temp list to store pandas dataframe from quandl
# USD as based currency
currencies = ['CAD', 'AUD', 'HKD', 'EUR', 'GBP', 'JPY', 'MXN', 'CHF']
for currency in currencies:
    temp.append(quandl.get('CUR/'+currency, start_date=start, end_date=end))
temp_df = pd.concat(temp, axis=1)
temp_df.columns = currencies
store['fx'] = temp_df

# commodities historical data (daily - trading days)
temp = []
commodities = [#Barley, Corn, Rice, Soybeans, Wheat
               "ODA/PBARL_USD", "TFGRAIN/CORN.1", "ODA/PRICENPQ_USD", "TFGRAIN/SOYBEANS.1", "ODA/PWHEAMT_USD",
               #Sugar, Coffee Robusta, Cotton, Tea, Milk
               "CHRIS/ICE_SB1.1", "ODA/PCOFFROB_USD", "CHRIS/ICE_CT1.1", "ODA/PTEA_USD", "COM/MILK",
               #Bananas, Oranges, Peanuts
               "ODA/PBANSOP_USD", "ODA/PORANG_USD", "ODA/PGNUTS_USD",
               #Olive Oil, Palm Oil, Sunflower Oil, Rapeseed Oil 
               "ODA/POLVOIL_USD", "ODA/PPOIL_USD", "ODA/PSUNO_USD", "ODA/PROIL_USD",
               #Rubber, Soft Logs, Hard Logs, Hard Sawnwood, Soft Sawnwood
               "ODA/PRUBB_USD", "ODA/PLOGORE_USD", "ODA/PLOGSK_USD", "ODA/PSAWMAL_USD", "ODA/PSAWORE_USD",
               #Gold, Silver, Platinum, Palladium, Iron
               "COM/AU_EIB", "COM/AG_EIB", "COM/PL_EIB", "COM/PA_EFP", "COM/FE_TJN",
               #Aluminum, Cobalt, Copper, Lead, Nickel, Steel Billet, Tin, Zinc
               "LME/PR_AL.1", "LME/PR_CO.1", "LME/PR_CU.1", "LME/PR_PB.1", "LME/PR_NI.1", "LME/PR_FM.1", "LME/PR_TN.1", "LME/PR_ZI.1",
               #WTI Crude, Brent Crude, Dubai Crude, Natural Gas
               "EIA/PET_RWTC_D", "EIA/PET_RBRTE_D", "ODA/POILDUB_USD", "OPEC/ORB","CHRIS/CME_NG1.1"]
for commodity in commodities:
    temp.append(quandl.get(commodity, start_date=start, end_date=end))
temp_df = pd.concat(temp, axis=1)
temp_df.columns = commodities
store['commodities'] = temp_df

#

# macroeconomic data
# monthly
monthly = [#Japan: CPI (Energy), CPI (Food), Harmonized Unemployment Rate, Discount Rate
		   "FRED/JPNCPIENGMINMEI", "FRED/JPNCPIFODMINMEI", "FRED/JPNURHARMQDSMEI", "FRED/INTDSRJPM193N", 

		  ]
temp = []
for month in monthly:
    temp.append(quandl.get(month, start_date=start, end_date=end))
temp_df = pd.concat(temp, axis=1)
temp_df.columns = monthly
store['macro_monthly'] = temp_df


# quarterly
quarterly = [# Canada:
		  # Australia: 
		  # Hong Kong: 
		  # Europe: 
		  # UK: 
		  # Japan: GDP (in JPY)
			'FRED/JPNRGDPQDSNAQ',
		  # Mexico:
		  # Switzerland:
		  ]
temp = []
for quarter in quarterly:
    temp.append(quandl.get(quarter, start_date=start, end_date=end))
temp_df = pd.concat(temp, axis=1)
temp_df.columns = quarterly
store['macro_quarterly'] = temp_df