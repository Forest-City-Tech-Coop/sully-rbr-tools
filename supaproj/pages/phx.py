import base64
import io
import dash
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State
import pandas as pd

dash.register_page(__name__)

layout = html.Div([
    html.H2("Upload CSV and Display DataFrame"),
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select CSV File')]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # set True if you want multiple file uploads
    ),
    html.Div(id='output-data-upload')
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            return html.Div(["Unsupported file format."])

    except Exception as e:
        return html.Div([f"There was an error processing this file: {e}"])
    # format the data
    ## add id
    new_rows = [{"Location": "Residential Collections", "Item Variation": "Consignment Fee", "Item Name": "RBR"}, {"Location": "Soil Blends", "Item Variation": "Consignment Fee", "Item Name": "RBR"}]
    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    df["id"] = filename




    ## clean data for dollar signs and cast to floats
    money_columns = ['Items Sold', 'Items Refunded', 'Units Sold', 'Units Refunded', 'Gross Sales', 'Refunds', 'Discounts & Comps', 'Net Sales', 'Tax']
    int_columns = ["Location", "Item Name", "Item Variation", "SKU", "Category", "Unit"]

    for col in money_columns:
        df[col] = df[col].replace(r'[\$,]', '', regex=True).astype(float)
    for col in int_columns:
        df[col] = df[col].astype(str)

    # create data groupings
    groups = df.groupby(["Item Name","id"], as_index=False)[["Gross Sales"]].sum()

    total = df["Gross Sales"].sum()
    consign = .85
    fee = total - (total * consign)
    groups["Item Variation"] = "Consignment Fee"
    groups["Consignment Fee"] = (groups["Gross Sales"] / groups["Gross Sales"].sum()) * fee
    groups["Expected Check Total"] = total - groups['Consignment Fee'].sum() 

    res_fee = groups.loc[groups["Item Name"] == "RBR"]["Consignment Fee"]
    print(float(res_fee))
    df.loc[df["Location"] == "Residential Collections", "Gross Sales"] = float(res_fee)
    print(res_fee)
    phx_txn = {}
    phx_txn.update({"id": filename, "consignment fee": fee, "Residential Fee": float(res_fee.iloc[0]), "Soil Fee": fee - float(res_fee.iloc[0]) })
    # phx_txn["Residential Fee"] = 5
    # phx_txn["Soil Fee"] = 5
    print(phx_txn)
    print(df)

    # Return as DataTable
    return html.Div([
        html.H5(filename),
        dash_table.DataTable(
            data=groups.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in groups.columns],
            page_size=10,
            style_table={'overflowX': 'auto'}
        ),
    ])

@callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        return parse_contents(contents, filename)
