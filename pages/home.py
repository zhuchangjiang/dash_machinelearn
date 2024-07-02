# pages/home.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = dbc.Container([
    html.H1("Welcome to ML Workflow Designer", className="text-center my-4"),
    html.P("Create, manage, and run machine learning workflows with ease.", className="text-center"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Create Workflow", className="card-title"),
                html.P("Design your ML workflow using our intuitive drag-and-drop interface."),
                dbc.Button("Start Designing", href="/workflow-designer", color="primary"),
            ])
        ]), width=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("View Results", className="card-title"),
                html.P("Analyze the results of your ML workflows."),
                dbc.Button("View Results", href="/results", color="primary"),
            ])
        ]), width=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Documentation", className="card-title"),
                html.P("Learn how to use the ML Workflow Designer effectively."),
                dbc.Button("Read Docs", href="#", color="primary"),
            ])
        ]), width=4),
    ], className="my-4")
])