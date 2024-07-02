# pages/documentation.py
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/documentation')

layout = dbc.Container([
    html.H1("Documentation", className="text-center my-4"),
    dbc.Row([
        dbc.Col(
            dbc.Nav([
                dbc.NavLink("Getting Started", href="#getting-started", active="exact"),
                dbc.NavLink("Workflow Designer", href="#workflow-designer", active="exact"),
                dbc.NavLink("Node Types", href="#node-types", active="exact"),
                dbc.NavLink("Running Workflows", href="#running-workflows", active="exact"),
            ],
            vertical=True,
            pills=True,
            ), width=3
        ),
        dbc.Col([
            html.H2("Getting Started", id="getting-started"),
            html.P("Welcome to the ML Workflow Designer. This tool allows you to create, manage, and run machine learning workflows with ease."),
            html.H2("Workflow Designer", id="workflow-designer"),
            html.P("The Workflow Designer page is where you can create your ML workflows using a drag-and-drop interface."),
            html.H2("Node Types", id="node-types"),
            html.P("There are several types of nodes available, including data processing, feature engineering, model training, and evaluation nodes."),
            html.H2("Running Workflows", id="running-workflows"),
            html.P("Once you've designed your workflow, you can run it and view the results on the Results page."),
        ], width=9)
    ])
])