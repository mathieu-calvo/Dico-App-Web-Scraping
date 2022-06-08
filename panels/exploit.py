# -*- coding: utf-8 -*-
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app

layout = [
    dbc.Container([
        dbc.Row([
            dbc.Col([html.Div("Content not created yet")], width=8, className="pretty_container"),
        ]),
        dbc.Row([
            dbc.Col([html.Div("Content not created yet")], width=6, className="pretty_container"),
        ]),
        dbc.Row([
            dbc.Col([html.Div("Content not created yet")], width=3, className="pretty_container"),
        ]),
        dbc.Row([
            dbc.Col([html.Div("Content not created yet")], width=5, className="pretty_container"),
        ]),
        dbc.Row([
            dbc.Col([html.Div("Content not created yet")], width=12, className="pretty_container"),
        ]),
    ]),
]
