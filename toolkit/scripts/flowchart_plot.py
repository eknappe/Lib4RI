# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 11:16:58 2025

@author: knappeel

Toolkit hierachy category visualizations
Create and interactive html figure that allows users to navigate through the
categories and find tools to help them with different steps of the research 
process -- but based on the library services provided by lib4ri

Plotly page on sunburst charts : https://plotly.com/python/sunburst-charts/#sunburst-of-a-rectangular-dataframe-with-plotlyexpress

.
"""

## Toolkit visualizations  ##

## Import the necessary libraries 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import os
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

from dash import Dash, dcc, html, Input, Output, callback_context
import webbrowser

### Set working directory -- python scripts are hosted in within a folder in this directory
### Going to be two folders in horizontal -- data and python
working_directory = "\\Users\\knappeel\\Documents\\library\\coding\\toolkit"
os.chdir(working_directory)

## Where to save
save_directory=(working_directory+'\\data\\')
figsave_directory=(working_directory+'\\data\\output\\')
# if save folder does not exist, create it
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

node_filename = (save_directory + 'categories_sunburst.csv')

#### Step up the parent child relationships
### Import from a spreadsheet -- this spreadsheet setups up the relationships
### so it is slightly confusing
### id = parent label + label (top top level, would only have id and label no parent_id)
### label = name to display
### parent_id = parent id
### color = the shade you want that piece of the pie chart to be
### shade_tier = to help me organize the colors

## import the dataset
node_df = pd.read_csv(node_filename)

# Create the Dash app
app = Dash(__name__)

## make the figure

fig = go.Figure()

fig.add_trace(go.Sunburst(
    ids=node_df.ids,
    labels=node_df.labels,
    parents=node_df.parent_id,
    domain=dict(column=1),
    maxdepth=2,
    marker=dict(colors=node_df.color),
    customdata=node_df.link,
    hovertemplate='<b>Click to discover tools</b><extra></extra>',
    rotation=150
))

fig.update_layout(
    margin = dict(t=10, l=10, r=10, b=10)
)

## create the 'app' layout within dash
app.layout = html.Div([
    html.H1("A Researcher's Toolkit"),
    dcc.Graph(
        id='sunburst-graph',
        figure=fig
    ),
    html.Div(id='click-output')
])

## define callback to handle click events
@app.callback(
    Output('click-output', 'children'),
    Input('sunburst-graph', 'clickData')
)
def display_click_data(clickData):
    if clickData is None:
        return "Click on a segment to open its resource"
    
    ## get the link from the customdata
    link = clickData['points'][0]['customdata']
    
    if link and link != '' and not pd.isna(link):
        ## open the link in a new tab
        webbrowser.open_new_tab(link)
        return f"Opening: {link}"
    else:
        return "No link available for this item"

# Run the app
if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=True)




