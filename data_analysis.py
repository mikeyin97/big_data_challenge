# Importing Relevant Libraries
import pandas as pd
import numpy as np
import os
import inspect
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn import datasets, linear_model
import seaborn as sns
import warnings

# Initial calls
plt.ion()
sns.set()
warnings.filterwarnings("ignore",".*GUI is implemented.*")

# Function Definitions
def log(column):        #takes the natural log of each value of the input column
    column += 0.0001
    return (np.log2(column))

def animate_one(col, size):
    plt.legend(handles=[blue_patch, green_patch, red_patch, cyan_patch, mag_patch, yel_patch])
    result_by_year = result[result['year'] == year]
    plt.title(str(year) + " " + col)
    plt.scatter(x = log(result_by_year[col]), y = log(result_by_year['e_inc_100k']), c = result["color"].values.tolist(), alpha = 0.8)
    plt.axis(size)
    plt.xlabel("log " + col)
    plt.ylabel("log incidence/100k")
    plt.draw()

def animate_plot(col, axes):
    while True:
        for year in years:
            plt.legend(handles=[blue_patch, green_patch, red_patch, cyan_patch, mag_patch, yel_patch])
            result_by_year = result[result['year'] == year]
            plt.title(year)
            #plt.plot(log(result_by_year[col]),log(result_by_year['e_inc_100k']), "x", color=colors[(year-2000)%len(colors)])
            plt.scatter(x = log(result_by_year[col]), y = log(result_by_year['e_inc_100k']), c = result["color"].values.tolist(), alpha = 0.8)
            plt.axis(axes)
            plt.xlabel("log pop dens")
            plt.ylabel("log incidence/100k")
            plt.draw()
            plt.pause(pause_time)
            plt.clf() #I have yet to figure out how to exit this loop
    

# Constant Variables
colors = ["b", "g", "r", "c", "m", "y", "k", "#22ff00"]         # Colour List to cycle
axis_pop_dens = (-2, 20, -2, 12)                         # Axes Parameters
axis_health_exp = (-6, 25, -5, 25)
axis_gdp = (0, 20, -2, 20)
pause_time = 0.5                                                # Time between graph cycles
blue_patch = mpatches.Patch(color='b', label='Europe')
green_patch = mpatches.Patch(color='g', label='Africa')
red_patch = mpatches.Patch(color='r', label='Americas')
cyan_patch = mpatches.Patch(color='c', label='Western Pacific')
mag_patch = mpatches.Patch(color='m', label='Eastern Mediterranean')
yel_patch = mpatches.Patch(color='y', label='Southeast Asia')


# Setting Directory Path
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))

# Generating Dataframes for TB and Population Density Data
tb_data = pd.read_csv(module_dir+'/datasets/TB_burden_countries_2017-05-16.csv')
pop_den_data = pd.read_csv(module_dir+'/datasets/Pop_dens_by_country.csv', encoding="cp1252")
gdp_data = pd.read_excel(module_dir+'/datasets/GDP_percapita.xlsx')
health_data = pd.read_excel(module_dir+'/datasets/Expend_Percapita.xlsx')
health_data = health_data.loc[1:]
gdp_data = gdp_data[1:]

# Dataframe Selection of Relevant Columns
tb_data_less = tb_data[["iso3", "year", "e_inc_100k", "g_whoregion"]]
pop_den_data_less = pop_den_data[["Country Name", "Country Code", "2000", "2001", "2002", "2003", 
"2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013",
"2014", "2015"]]

# Match health and gdp data to shape of TB Data DF
health_data_less = pd.melt(health_data, var_name= "year", id_vars = ["Countries", "Indicators", "Units"], value_name = "Data")
health_data_less = health_data_less.sort_values(by = ['Countries', 'year'], ascending=True)
health_data_less['year'] = health_data_less['year'].astype(int)
health_data_less["Data"] = [float("NaN") if type(i) == str else i for i in health_data_less["Data"]]
health_data_less = health_data_less.rename(columns={"Data": "Health Expenditure per capita"})

gdp_data_less = pd.melt(gdp_data, var_name= "year", id_vars = ["Countries", "Indicators", "Units"], value_name = "Data")
gdp_data_less = gdp_data_less.sort_values(by = ['Countries', 'year'], ascending=True)
gdp_data_less['year'] = gdp_data_less['year'].astype(int)
gdp_data_less["Data"] = [float("NaN") if type(i) == str else i for i in gdp_data_less["Data"]]
gdp_data_less = gdp_data_less.rename(columns={"Data": "GDP per capita"})

# Match Population Density DF to Shape of TB Data DF -> Make the Years column
# into a Variable
pop_den_data_less = pd.melt(pop_den_data_less, id_vars=["Country Name", "Country Code"], 
                  var_name="Year", value_name="Population Density")
pop_den_data_less = pop_den_data_less.sort_values(by = ['Country Code', 'Year'], ascending=True)
pop_den_data_less = pop_den_data_less.rename(columns={"Country Name": "Countries", 'Country Code': 'iso3', 'Year': 'year'})
pop_den_data_less['year'] = pop_den_data_less['year'].astype(int)

# Join Dataframes at Common Year and Country Code
result = pd.merge(pop_den_data_less, tb_data_less, on=['year', 'iso3'])
result = pd.merge(result, health_data_less, on= ["Countries", "year"])
result = pd.merge(result, gdp_data_less, on= ["Countries", "year"])
print(result.iloc[0])

# Take the Log Values and Plot
"""logval = log(result["Population Density"])
logval2 = log(result['e_inc_100k'])
plt.figure(1)
plt.axis((xmin,xmax,ymin,ymax))
plt.scatter(logval, logval2)
plt.xlabel("log pop dens")
plt.ylabel("log incidence/100k")
plt.show()"""

# Generate a List of Relevant Years
years = list(range(min(result["year"]), max(result["year"])+1))


# Region Colors
region_colors = ["b", "g", "r", "c", "m", "y", "w"]
#set to white to isolate region 
#print(result["g_whoregion"].value_counts())
region_list = []
for i in (result["g_whoregion"]):
    if i == "EUR":
        region_list.append(region_colors[0])
    if i == "AFR":
        region_list.append(region_colors[1])
    if i == "AMR":
        region_list.append(region_colors[2])
    if i == "WPR":
        region_list.append(region_colors[3])
    if i == "EMR":
        region_list.append(region_colors[4])
    if i == "SEA":
        region_list.append(region_colors[5])
result["color"] = pd.DataFrame(region_list)

# Animate the Plot Year over Year
"""
#plt.figure(2)
#animate_plot("Population Density", axis_pop_dens)

plt.figure(3)
animate_plot('Health Expenditure per capita', axis_health_exp)

#plt.figure(4)
#animate_plot('GDP per capita', axis_gdp)
"""

# All 3?
try:
    while True:
        for year in years:
            plt.figure(2)
            animate_one("Population Density", axis_pop_dens)
            plt.figure(3)
            animate_one("Health Expenditure per capita", axis_health_exp)
            plt.figure(4)
            animate_one("GDP per capita", axis_gdp)
            plt.pause(pause_time)
            plt.figure(2)
            plt.clf() 
            plt.figure(3)
            plt.clf() 
            plt.figure(4)
            plt.clf() 
except KeyboardInterrupt:
    plt.clf() 





#Testing
#print(pop_den_data.shape)
#print(pop_den_data.columns.values)
#print(tb_data.columns.values)
#print(pop_den_data[["country"]])







