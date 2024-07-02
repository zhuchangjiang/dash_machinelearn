# components/sidebar.py
import dash_bootstrap_components as dbc
from dash import html

sidebar = html.Div([
    html.H4("Component Library", className="mb-3 text-primary"),
    html.Hr(),
    dbc.Nav([
        dbc.NavItem(dbc.NavLink("Data Processing", href="#")),
        dbc.NavItem(dbc.NavLink("Feature Engineering", href="#")),
        dbc.NavItem(dbc.NavLink("Model Training", href="#")),
        dbc.NavItem(dbc.NavLink("Evaluation", href="#")),
    ], vertical=True, pills=True),
], className="bg-light p-3 h-100")