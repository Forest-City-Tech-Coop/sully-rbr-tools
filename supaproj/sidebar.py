import dash_bootstrap_components as dbc
from dash import html

def sidebar():
    return dbc.Nav(
        [
            dbc.NavLink("Home", href="/", active="exact"),
            # Add more links here
        ],
        vertical=True,
        pills=True,
    )
