from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv("data/stockdata2.csv", index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])

# Initialize app
app = Dash(__name__)

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

# Define the app
app.layout = html.Div(
    children=[
        html.Div(className='row', # Define the row elements
            children=[
                html.Div(className='four columns div-user-controls', # Define the left element
                children = [
                        html.H2('Dash - STOCK PRICES'),
                        html.P('''Visualising time series with Plotly - Dash'''),
                        html.P('''Pick one or more stocks from the dropdown below.'''),
                        html.Div(className='div-for-dropdown',
                            children=[
                                dcc.Dropdown(id='stockselector',
                                            options=get_options(df['stock'].unique()),
                                            multi=True,
                                            value=[df['stock'].sort_values()[0]],
                                            style={'backgroundColor': '#1E1E1E'},
                                            className='stockselector')
                                        ],
                            style={'color': '#1E1E1E'})
                    ]), 
                html.Div(className='eight columns div-for-charts bg-grey', # Define the right element
                children= [
                    dcc.Graph(id='timeseries',
                    config={'displayModeBar': False},
                    animate=True,
                    figure=px.line(df,
                                    x='Date',
                                    y='value',
                                    color='stock',
                                    template='plotly_dark').update_layout(
                                            {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
                            )
                ]) 
                ])
    ]) 

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
