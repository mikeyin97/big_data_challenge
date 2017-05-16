
#Importing Relevant Libraries
import pandas as pd
import numpy as np
import os
import inspect
import matplotlib.pyplot as plt
import cv2
plt.ion()

#taking a log
def log(column):
    return (np.log2(column))

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
logval = log(result["Population Density"])
logval2 = log(result['e_inc_100k'])

#plot
plt.figure(1)
plt.scatter(logval, logval2)
plt.xlabel("logval pop dens")
plt.ylabel("logval incidence/100k")
plt.show()

#list of years
years = list(range(min(result["year"]), max(result["year"])+1))
colors = ["b", "g", "r", "c", "m", "y", "k", "#eeefff"]

#plot by years
plt.figure(2)

while True:
    for year in years:
        result_by_year = result[result['year'] == year]
        plt.title(year)
        plt.plot(log(result_by_year["Population Density"]),log(result_by_year['e_inc_100k']), "x", color=colors[(year-2000)%7])
        plt.axis((0,15,0,12))
        plt.draw()
        plt.pause(0.1)
        plt.clf()




#Testing
#print(pop_den_data.shape)
#print(pop_den_data.columns.values)
#print(tb_data.columns.values)
#print(pop_den_data[["country"]])







