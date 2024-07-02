# components/node_config_panel.py
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback

node_config_panel = dbc.Card([
    dbc.CardHeader("Node Configuration"),
    dbc.CardBody([
        html.Div(id="node-config-content")
    ])
], id="node-config-panel", className="mt-3")

@callback(
    Output('node-config-content', 'children'),
    Input('cytoscape', 'tapNodeData')
)
def update_node_config(node_data):
    if not node_data:
        return "Please select a node to configure"
    
    node_type = node_data.get('type', '')
    
    if node_type == '数据处理':
        return dbc.Form([
            dbc.FormGroup([
                dbc.Label("Select Data Source"),
                dcc.Dropdown(
                    id="data-source-select",
                    options=[{"label": src, "value": src} for src in data_sources.keys()],
                    value=list(data_sources.keys())[0]
                )
            ]),
            dbc.FormGroup([
                dbc.Label("Select Fields"),
                dcc.Checklist(
                    id="field-checklist",
                    options=[{"label": field, "value": field} for field in data_sources[list(data_sources.keys())[0]]],
                    value=[]
                )
            ])
        ])
    # ... (similar structures for other node types)
    
    return dbc.Form([
        dbc.FormGroup([
            dbc.Label("Node Name"),
            dbc.Input(id="node-name-input", type="text", value=node_data['label'])
        ]),
        dbc.FormGroup([
            dbc.Label("Node Description"),
            dbc.Textarea(id="node-description-input", placeholder="Enter node description")
        ]),
        dbc.Button("Update Node", id="update-node-button", color="primary", className="mt-3")
    ])

# Add callback to update node properties
@callback(
    Output('cytoscape', 'elements'),
    Input('update-node-button', 'n_clicks'),
    State('node-name-input', 'value'),
    State('node-description-input', 'value'),
    State('cytoscape', 'tapNodeData'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def update_node_properties(n_clicks, node_name, node_description, tapped_node, elements):
    if not n_clicks or not tapped_node:
        return dash.no_update
    
    for element in elements:
        if element['data']['id'] == tapped_node['id']:
            element['data']['label'] = node_name
            element['data']['description'] = node_description
            break
    
    return elements