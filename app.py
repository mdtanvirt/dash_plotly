
from dash import Dash, dash_table, html, dcc
import pandas as pd
import json
import dash_table as dt

with open('data/trips.json','r') as f:
    data = json.loads(f.read())
    
# Normalizing data
df = pd.json_normalize(data, record_path =['features'])

app = Dash(__name__)

app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

if __name__ == '__main__':
    app.run_server(debug=True)