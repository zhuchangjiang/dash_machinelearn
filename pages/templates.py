# pages/templates.py
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/templates')

templates = [
    {"name": "Basic Classification", "description": "A simple classification workflow"},
    {"name": "Image Recognition", "description": "Workflow for image classification tasks"},
    {"name": "Time Series Forecasting", "description": "Predict future values based on historical data"},
]

layout = dbc.Container([
    html.H1("Workflow Templates", className="text-center my-4"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4(template["name"], className="card-title"),
                html.P(template["description"]),
                dbc.Button("Use Template", href=f"/workflow-designer?template={template['name']}", color="primary"),
            ])
        ]), width=4) for template in templates
    ])
])

@callback(
    Output('cytoscape', 'elements'),
    Input('url', 'search')
)
def load_template(search):
    template_name = search.split('=')[-1] if search else None
    if template_name:
        # Load and return the appropriate template
        # For now, we'll just return a sample template
        return [
            {'data': {'id': 'node1', 'label': 'Data Source'}},
            {'data': {'id': 'node2', 'label': 'Preprocessing'}},
            {'data': {'id': 'node3', 'label': 'Model Training'}},
            {'data': {'source': 'node1', 'target': 'node2'}},
            {'data': {'source': 'node2', 'target': 'node3'}}
        ]
    return []