
#Importing Relevant Libraries
import matplotlib.pyplot as plt
import pandas as pd
import random
import datetime
import numpy as np
import math
import cv2
import os
import inspect
import os

#Setting Path
module_path = inspect.getfile(inspect.currentframe())
module_dir = os.path.realpath(os.path.dirname(module_path))
#print(module_dir)

#Making Dataframe
df = pd.read_csv(module_dir+'/datasets/TB_burden_countries_2017-05-16.csv')


