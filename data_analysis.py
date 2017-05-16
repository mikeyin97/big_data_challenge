
#Importing Relevant Libraries
import pandas as pd
import numpy as np
import os
import inspect
import matplotlib.pyplot as plt


#Setting Path
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))

#Making Dataframes
tb_data = pd.read_csv(module_dir+'/datasets/TB_burden_countries_2017-05-16.csv')
pop_den_data = pd.read_csv(module_dir+'/datasets/Pop_dens_by_country.csv', encoding="cp1252")

#Dataframe Selection
tb_data_less = tb_data[["iso3", "year", "e_inc_100k"]]
pop_den_data_less = pop_den_data[["Country Code", "2000", "2001", "2002", "2003", 
"2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013",
"2014", "2015"]]
#print(pop_den_data_less)

#Match pop den df to shape of tb data df -> verticalize years
pop_den_data_less = pd.melt(pop_den_data_less, id_vars=["Country Code"], 
                  var_name="Year", value_name="Population Density")
pop_den_data_less = pop_den_data_less.sort(['Country Code', 'Year'], ascending=True)
pop_den_data_less = pop_den_data_less.rename(columns={'Country Code': 'iso3', 'Year': 'year'})
pop_den_data_less['year'] = pop_den_data_less['year'].astype(int)

#Join dataframes
result = pd.merge(pop_den_data_less, tb_data_less, on=['year', 'iso3'])
log = (np.log(result["Population Density"]))
log2 = (np.log(result['e_inc_100k']))

#plot
plt.scatter(log, log2)
plt.xlabel("log pop dens")
plt.ylabel("log incidence/100k")
plt.show()

#Testing
#print(pop_den_data.shape)
#print(pop_den_data.columns.values)
#print(tb_data.columns.values)
#print(pop_den_data[["country"]])







