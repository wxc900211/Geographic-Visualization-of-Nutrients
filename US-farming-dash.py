#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[46]:


from pandas_geojson import read_geojson
geojson = read_geojson('US-map.geojson')


# In[48]:


names_to_remove = ["Puerto Rico", "Alaska", "Hawaii"]
filtered_features = [feature for feature in geojson['features'] if feature['properties']['NAME'] not in names_to_remove]

# Replace the old features with the filtered ones
geojson['features'] = filtered_features


# In[36]:


df = pd.read_csv('E.csv')


# In[42]:


df = pd.read_csv('E.csv')
df = df[~df['NAME'].isin(['Puerto Rico', 'Alaska', "Hawaii"])]


# In[ ]:


fig = px.choropleth_mapbox(
        df, geojson=geojson, color=candidate,
        locations="district", featureidkey="properties.district",
        center={"lat": 45.5517, "lon": -73.7073}, zoom=9,
        range_color=[0, 6500])
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken=token)


# In[53]:


from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Nutrients Data Analysis'),
    html.P("Select a element:"),
    dcc.RadioItems(
        id='element', 
        options=["E1", "E2" ],
        value="E1",
        inline=True
    ), 
    dcc.Graph(id="graph"),
    dcc.Slider(
        df['Year'].min(),
        df['Year'].max(),
        step=None,
        id='year--slider',
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()}
    )
],style={'width': '80%', 'float': 'left', 'display': 'inline-block', 'font-family':'Arial'})


@app.callback(
    Output("graph", "figure"), 
    Input("element", "value"),
    Input("year--slider", "value"))

def display_choropleth(element,year_value):
    dff = df[df['Year'] == year_value]
    fig = px.choropleth(dff, geojson=geojson, color=element,
                    locations="NAME",featureidkey="properties.NAME",
                    color_discrete_sequence= px.colors.sequential.Plasma_r,projection="mercator"
                   )
        
    fig.update_geos(fitbounds="geojson", visible=False)
    fig.update_layout(autosize=False,margin={"r":0,"t":0,"l":0,"b":0},width=800,height=500)

    
    return fig


app.run_server(debug=True)


# In[54]:


server = app.server


# In[ ]:




