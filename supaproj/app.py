import os
import sys
from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
from flask import Flask, request, Blueprint
import plotly.express as px
from webhook_storage import webhook_data_storage

load_dotenv()
server = Flask(__name__)
webhook_bp = Blueprint('webhook_bp', __name__)

@server.route("/webhook_listener", methods=["GET", "POST"])
def webhook_listener():
    if request.method == "POST":
        print("Received:", request.get_json())
        return "OK", 200
    return "Webhook endpoint alive", 200

server.register_blueprint(webhook_bp)

######set up clients
####### Supabase
url: str = os.environ.get("SUPABASE_URL") #type: ignore
key: str = os.environ.get("SUPABASE_KEY") #type: ignore

if not url or not key:
    print("Environment variables SUPABASE_URL or SUPABASE_KEY are not set.")
    sys.exit(1) 

supabase: Client = create_client(url, key)

######## Dash app
import dash
from dash import Dash, dcc, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
app = Dash(__name__, server=server, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
port = 8080
host = "0.0.0.0"

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
        .select("route_id, timestamp_date, stop_id, vehicle", count="exact") # type: ignore
        .gte("timestamp_date", "2024-08-01")
        .in_("vehicle", res_vehicles)
        .range(start, end)
        .execute()
    )
    data = response.data
    if not data:
        break
    all_data.extend(data)
    if len(all_data) >= response.count: # type: ignore
        break
    page_number += 1

df = pd.DataFrame(all_data)

dfgri = df.groupby("vehicle")
dfgric = dfgri.count()


headers = dfgric.columns.to_list()
#### webapp structure

##### main page layout

### `dash.page_container` is where selected pages will fill in. the rest of the explicitly defined html will will render around it 
app.layout = html.Div([
        html.H1("Look at all the data!!"),
        dcc.Interval(id="webhook-interval",interval=100,n_intervals=0),
        html.Div(id="webhook-display"),
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
            port=port,host=host)
