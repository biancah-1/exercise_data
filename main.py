import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from jefit_data_func import *
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
df_workouts_filt = df_workouts.loc[(df_workouts['Date'].dt.year==2023) & (df_workouts['Date'].dt.month>=5) & (df_workouts['Num_Exercises']>=5)]
dates = df_workouts_filt['Date'].dt.date

# selecting dates in exercise logs
mask = (df_exercise['Date'].dt.date).isin(dates)
df_exercise_filt = df_exercise[mask]

# filtering to include 5 most common exercises
ex_counts = df_exercise_filt['Exercise_Name'].value_counts()
ex_name = ex_counts.loc[ex_counts>10].index.tolist()

ex_mask = (df_exercise_filt['Exercise_Name']).isin(ex_name)
df_exercise_data = df_exercise_filt[ex_mask]

# adding calculated values
df_exercise_data['Weight_Max'],df_exercise_data['Volume_Sets'], df_exercise_data['Volume_Total'] = zip(*df_exercise_data['Exercise_Logs'].apply(weight_calcs))

# removing time, keeping just date
df_exercise_data['Date'] = df_exercise_data['Date'].dt.date 

'''
top5_ex_name = ex_counts.head(5).index.tolist()
ex_mask = (df_exercise_filt['Exercise_Name']).isin(top5_ex_name)
df_exercise_top5 = df_exercise_filt[ex_mask]

# adding calculated values 
df_exercise_top5['Weight_Max'],df_exercise_top5['Volume_Sets'], df_exercise_top5['Volume_Total'] = zip(*df_exercise_top5['Exercise_Logs'].apply(weight_calcs))

# removing time, keeping just date
df_exercise_top5['Date'] = df_exercise_top5['Date'].dt.date 
'''

# Dash App for Displaying data
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Exercise Tracker'),
    dcc.Dropdown(ex_name, 'Barbell Bench Press',id='dropdown'),
    dcc.Graph(id='graph-content')
    ])

@callback(
    Output('graph-content','figure'),
    Input('dropdown','value')
)

def update_graph(value):
    vals = df_exercise_data.loc[df_exercise_data['Exercise_Name']==value]
    dates = vals['Date']

    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(row=1, col=1,
                  trace = go.Scatter(x=dates,y=vals['Weight_Max'],mode='markers',name='Max Weight (lbs)')
                  )
    fig.add_trace(row=2, col=1,
                  trace = go.Scatter(x=dates,y=vals['Volume_Total'],mode='markers',name='Total Volume (lbs)')
                  )   
    return fig

if __name__ == '__main__':
    app.run(debug=True)
