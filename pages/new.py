import dash
from dash import callback, html, dcc, Input, Output

dash.register_page(__name__)

layout = html.Div([
    html.H1('This is a new page!'),
    dcc.DatePickerRange()
])