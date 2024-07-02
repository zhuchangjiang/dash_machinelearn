# app.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("New", href="/workflow-designer"),
                dbc.DropdownMenuItem("Open", id="open-workflow"),
                dbc.DropdownMenuItem("Save", id="save-workflow"),
                dbc.DropdownMenuItem("Import", id="import-workflow"),
                dbc.DropdownMenuItem("Export", id="export-workflow"),
            ],
            nav=True,
            in_navbar=True,
            label="Workflow",
        ),
        dbc.NavItem(dbc.NavLink("Results", href="/results")),
        dbc.NavItem(dbc.NavLink("Templates", href="/templates")),
        dbc.NavItem(dbc.NavLink("Documentation", href="/documentation")),
    ],
    brand="ML Workflow Designer",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    navbar,
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)