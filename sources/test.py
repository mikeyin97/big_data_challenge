# Importing Relevant Libraries
import pandas as pd
import numpy as np
import os
import inspect
import matplotlib.pyplot as plt
from sklearn import datasets, linear_model

# Constant Variables
colors = ["b", "g", "r", "c", "m", "y", "k", "#22ff00"]         # Colour List to cycle
xmin, xmax, ymin, ymax = -2, 15, -2, 12                         # Axes Parameters
pause_time = 0.5                                                # Time between graph cycles

# Setting Directory Path
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))

# Generating Dataframes for TB and Population Density Data
tb_data = pd.read_csv(module_dir+'/../datasets/TB_burden_countries_2017-05-16.csv')
pop_den_data = pd.read_csv(module_dir+'/../datasets/Pop_dens_by_country.csv', encoding="cp1252")

# Dataframe Selection of Relevant Columns
tb_data = tb_data[['g_whoregion', 'year', 'e_inc_100k']]
size = len(tb_data['g_whoregion'])
regions = tb_data['g_whoregion'].unique()
years = tb_data['year'].unique()
results = {}

#determining incident rates per world region
for region in regions:
    results[region] = {}
    for year in years:
        results[region][year] = [0, 0]


for i in range(size):
    results[tb_data['g_whoregion'][i]][tb_data['year'][i]][0] += tb_data['e_inc_100k'][i]
    results[tb_data['g_whoregion'][i]][tb_data['year'][i]][1] += 1

results_norm = {}
for key in results:
    results_norm[key] = []
    for year in years:
        print str(year) + ": " + str(results[key][year][0]/results[key][year][1])
        results_norm[key].append(results[key][year][0]/results[key][year][1])
        

print results_norm

# create plot
plt.figure(num=None, figsize=(18, 10), dpi=80, facecolor='w', edgecolor='w')
colors = {  'WPR': 'b',
            'EMR': 'g',
            'AMR': 'c',
            'AFR': 'k',
            'EUR': 'y',
            'SEA': 'm'}

bar_width = 0.10
index = np.arange(len(years))
count = 0
for region in regions:
    """
    plt.bar(index+count*bar_width, results_norm[region], bar_width, alpha = 0.5, color=colors[region], label=region)
    count += 1
    """
    plt.plot(years, results_norm[region], alpha=0.5, color= colors[region], label=region)

plt.xlabel('Year')
plt.ylabel('Incidences per 100 000 population')
plt.title('World Tuberculosis Incidences for the Past 15 Years')
#plt.xticks(index+bar_width*(len(regions)-1)/2, years)
plt.legend()
plt.show()
