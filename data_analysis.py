
#Importing Relevant Libraries
import pandas as pd
import numpy as np
import os
import inspect

#Setting Path
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
#print(module_dir)

#Making Dataframe
df = pd.read_csv(module_dir+'/datasets/TB_burden_countries_2017-05-16.csv')
print(df.describe())
print(df.columns.values)

#Dataframe Testing
df2 = df[["iso2", "e_pop_num"]]
print(df2)



