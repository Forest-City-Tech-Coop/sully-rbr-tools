import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from ..sidebar import sidebar
from ..webhook_storage import webhook_data_storage
import json

dash.register_page(__name__, path="/")  # register for multipage

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(sidebar(), width=2),
                dbc.Col(
                    html.Div(
                        [
                            html.H1("Webhook Dashboard"),
                            html.Div(id="webhook-display"),
                        ]
                    ),
                    width=10,
                ),
            ]
        ),
        dcc.Interval(id="interval-component", interval=5*1000, n_intervals=0),
    ]
)


# Callback to update webhook display
@dash.callback(
    Output("webhook-display", "children"),
    Input("interval-component", "n_intervals")
)
def display_webhook(n_intervals):
    if not webhook_data_storage:
        return "Waiting for webhook data..."
    return html.Pre(json.dumps(webhook_data_storage, indent=2))
