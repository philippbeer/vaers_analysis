#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import config as cnf
import data_processing as dp_vaers

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# get data
df = dp_vaers.get_all_vaers_data()
df['RECVYEAR'] = df['RECVDATE'].dt.year

# create adverse events per age group 
df_yrly = df.groupby(['RECVYEAR', 'AGE_BINS'])['VAERS_ID'].count().reset_index()
df_cur_yr = df_yrly[df_yrly['RECVYEAR']==2021]
df_yrly_prev_mean =  df_yrly[df_yrly['RECVYEAR']<2021].groupby(['AGE_BINS']).mean().reset_index()

hist_age_group = go.Figure()
hist_age_group.add_trace(go.Bar(x=df_yrly_prev_mean['AGE_BINS'],
                     y=df_yrly_prev_mean['VAERS_ID'],
                     name='Years prior 2021 (mean)'))
hist_age_group.add_trace(go.Bar(x=df_cur_yr['AGE_BINS'],
                     y=df_cur_yr['VAERS_ID'],
                     name='2021 (abs)'))
hist_age_group.update_layout(
    title = "Adverse Event by Age Group prior 2021 (mean) and 2021 (abs)",
    xaxis_title = "Age Group",
    yaxis_title = "# adverse events",
    legend_title = "Legend"
    
)

# percentage of deaths on total adverse events
df_yr_died = df.groupby(['RECVYEAR', 'DIED'])['VAERS_ID'].count()
df_died_perc = df_yr_died.groupby(level=0)\
                         .apply(lambda x: x * 100 / float(x.sum()))\
                         .reset_index()

df_died_ts = df_died_perc[(df_died_perc['DIED']=="Y")]
fig_died_ts = px.area(df_died_ts,
                      x='RECVYEAR', y='VAERS_ID')


app.layout = html.Div(children=[
    html.H1(children='VAERS Data Analysis'),
    html.Div(children='''
    VAERS: Analysis of the data from June 18th 2021
    '''),
    dcc.Graph(
        id='hist',
        figure=hist_age_group
    ),
    dcc.Graph(
        id='ts-died',
        figure=fig_died_ts
    )
])

if __name__ == "__main__":
    app.run_server(debug=True)
