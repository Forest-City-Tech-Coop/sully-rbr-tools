import dash
from dash import callback, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from .sidebar import sidebar
dash.register_page(__name__, path="/")


# def layout(**kwargs):
#     return dbc.Row(
#         [dbc.Col(sidebar(), width=2), dbc.Col(html.Div(
#             html.H1("This is the homepage")))]
#     )
layout = html.Div(
    html.H1('This is the homepage!')
)