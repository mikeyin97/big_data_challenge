# Importing Relevant Libraries
import pandas as pd
import numpy as np
import os
import inspect
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model
plt.ion()

# Function Definitions
def log(column):        #takes the natural log of each value of the input column
    return (np.log2(column))
    
# Constant Variables
colors = ["b", "g", "r", "c", "m", "y", "k", "#22ff00"]         # Colour List to cycle
xmin, xmax, ymin, ymax = -2, 15, -2, 12                         # Axes Parameters
pause_time = 0.5                                                # Time between graph cycles

# Setting Directory Path
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))

# Generating Dataframes for TB and Population Density Data
tb_data = pd.read_csv(module_dir+'/datasets/TB_burden_countries_2017-05-16.csv')
pop_den_data = pd.read_csv(module_dir+'/datasets/Pop_dens_by_country.csv', encoding="cp1252")

# Dataframe Selection of Relevant Columns
tb_data_less = tb_data[["iso3", "year", "e_inc_100k"]]
pop_den_data_less = pop_den_data[["Country Code", "2000", "2001", "2002", "2003", 
"2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013",
"2014", "2015"]]
#print(pop_den_data_less)

# Match Population Density DF to Shape of TB Data DF -> Make the Years column
# into a Variable
pop_den_data_less = pd.melt(pop_den_data_less, id_vars=["Country Code"], 
                  var_name="Year", value_name="Population Density")
pop_den_data_less = pop_den_data_less.sort(['Country Code', 'Year'], ascending=True)
pop_den_data_less = pop_den_data_less.rename(columns={'Country Code': 'iso3', 'Year': 'year'})
pop_den_data_less['year'] = pop_den_data_less['year'].astype(int)

# Join Dataframes at Common Year and Country Code
result = pd.merge(pop_den_data_less, tb_data_less, on=['year', 'iso3'])

# Take the Log Values and Plot
logval = log(result["Population Density"])
logval2 = log(result['e_inc_100k'])
plt.figure(1)
plt.axis((xmin,xmax, ymin, ymax))
plt.scatter(logval, logval2)
plt.xlabel("log pop dens")
plt.ylabel("log incidence/100k")
plt.show()

# Generate a List of Relevant Years
years = list(range(min(result["year"]), max(result["year"])+1))

# Animate the Plot Year over Year
plt.figure(2)
while True:
    for year in years:
        result_by_year = result[result['year'] == year]
        plt.title(year)
        plt.plot(log(result_by_year["Population Density"]),log(result_by_year['e_inc_100k']), "x", color=colors[(year-2000)%len(colors)])
        plt.axis((xmin,xmax, ymin, ymax))
        plt.xlabel("log pop dens")
        plt.ylabel("log incidence/100k")
        plt.draw()
        plt.pause(pause_time)
        plt.clf() #I have yet to figure out how to exit this loop
plt.close()



#Testing
#print(pop_den_data.shape)
#print(pop_den_data.columns.values)
#print(tb_data.columns.values)
#print(pop_den_data[["country"]])







