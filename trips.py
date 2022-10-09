# Import necessary modules
from email.policy import default
from email.quoprimime import header_decode
from turtle import title
import dash
import json
from dash import dcc, html
from flask import Flask
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Initiate the app
server = Flask(__name__)
app = dash.Dash(__name__, server = server)

# Read the file and normalization & indexing
with open('data/trips.json', 'r') as f:
    data = json.loads(f.read())

# Normalize data
df = pd.json_normalize(data, record_path =['features'])

#convert data type
df['properties.starttime'] = pd.to_datetime(df['properties.starttime'])
df.astype({'geometry.coordinates':'string', 'geometry.type':'string', 'type':'string', 'properties.streetnames':'string', 'properties.taxiid':'string'}).dtypes

df.drop("geometry.coordinates", axis=1, inplace=True)
df.drop("properties.streetnames", axis=1, inplace=True)

# Set index
df = df.set_index('properties.tripid')

# Build the components
header_component = html.H1("Trips Analysis Dashboard", style={'color':'darkcyan'})

# Visual component
# Component-1
countfig = go.FigureWidget()

countfig.add_scatter(name='Distance', x=df['properties.duration'], y=df['properties.maxspeed'].cumsum(), fill='tonexty')
countfig.add_scatter(name='Maxspeed', x=df['properties.duration'], y=df['properties.distance'].cumsum(), fill='tonexty')

countfig.update_layout(title='Distance Vs Maxspeed')

# Design the app layout
app.layout = html.Div(
    [
        dbc.Row([
            header_component
        ]),
        dbc.Row(
            [dbc.Col(
                [dcc.Graph(figure=countfig)]
            ), dbc.Col()]
        ),
        dbc.Row(
            [dbc.Col(), dbc.Col(), dbc.Col()]
        ),
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)