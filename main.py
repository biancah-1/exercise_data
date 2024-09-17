import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from jefit_data_func import *

# cleaning data for workouts
w_path = 'data\workout_logs.csv'
w_og = ['TIMESTAMP','total_exercise','total_weight','recordbreak']
w_new = ['Date','Num_Exercises','Total_Weight','Num_PRs']
df_workouts = clean_data(w_path,w_og,w_new)

# cleaning data for exercise logs
ex_path = 'data\exercise_logs.csv'
ex_og = ['TIMESTAMP','logs','ename']
ex_new = ['Date','Exercise_Logs','Exercise_Name']
df_exercise = clean_data(ex_path,ex_og,ex_new)

# filtering for July - Dec 2023, with 5 or more exercises in a session
df_workouts_filt = df_workouts.loc[(df_workouts['Date'].dt.year==2023) & (df_workouts['Date'].dt.month>=7) & (df_workouts['Num_Exercises']>=5)]
dates = df_workouts_filt['Date'].dt.date

# selecting dates in exercise logs
mask = (df_exercise['Date'].dt.date).isin(dates)
df_exercise_filt = df_exercise[mask]

# filtering to include 5 most common exercises
ex_counts = df_exercise_filt['Exercise_Name'].value_counts()
top5_ex_count = ex_counts.head(5).plot(kind='bar')
#plt.show()
top5_ex_name = ex_counts.head(5).index.tolist()
ex_mask = (df_exercise_filt['Exercise_Name']).isin(top5_ex_name)
df_exercise_top5 = df_exercise_filt[ex_mask]

# adding calculated values 
df_exercise_top5['Weight_Max'],df_exercise_top5['Volume_Sets'], df_exercise_top5['Volume_Total'] = zip(*df_exercise_top5['Exercise_Logs'].apply(weight_calcs))
