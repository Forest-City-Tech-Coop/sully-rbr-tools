import os
from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import json
from pprint import pprint
import dash
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px

load_dotenv()

######set up clients
####### Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

######## Dash app

app = Dash(__name__, use_pages=True)
port = 8050

##### Data Functions
page_size = 1000
page_number = 1
all_data = []

res_vehicles = ['Promaster', 'Promaster 2']

while True:
    start = (page_number - 1) * page_size
    end = start + page_size - 1
    
    response = (
        supabase.schema("rbr")
        .table("stops")
        .select("route_id, timestamp_date, stop_id, vehicle", count="exact")
        .gte("timestamp_date", "2025-08-01")
        .in_("vehicle", res_vehicles)
        .range(start, end)
        .execute()
    )
    data = response.data
    if not data:
        break
    all_data.extend(data)
    if len(all_data) >= response.count:
        break
    page_number += 1

df = pd.DataFrame(all_data)

dfgri = df.groupby("route_id")
dfgric = dfgri.count()


headers = dfgric.columns.to_list()
#### webapp structure

##### main page layout

### `dash.page_container` is where selected pages will fill in. the rest of the explicitly defined html will will render around it 
app.layout = html.Div([
        html.H1("Look at all the data!!"),
        dash_table.DataTable(
            id="table-container",
            columns=[{"name": i, "id": i} for i in headers],
            data=dfgric.to_dict('records'),
        ),
        html.Div([
        html.Nav(
            dcc.Link(f"{page['name']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
        ]),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run(debug=True,
            port=port)
