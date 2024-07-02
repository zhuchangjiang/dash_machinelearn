import dash
from dash import html, dcc, Input, Output, State, callback, ctx, no_update
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import json
import networkx as nx
from components.sidebar import sidebar
from components.node_config_panel import node_config_panel
from components.cytoscape_layout import cytoscape_layout

dash.register_page(__name__, path='/workflow-designer')

layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar, width=3, className="p-0"),
        dbc.Col([
            html.H2("Machine Learning Workflow Designer", className="text-center mb-4 text-primary"),
            dbc.Card([
                dbc.CardBody([
                    cytoscape_layout,
                    dbc.ButtonGroup([
                        dbc.Button("Connect Nodes", id="connect-nodes-button", color="primary", className="me-2"),
                        dbc.Button("Delete Selected", id="delete-selected-button", color="danger", className="me-2"),
                        dbc.Button("Run Workflow", id="run-flow-button", color="success", className="me-2"),
                        dbc.Button("Undo", id="undo-button", color="secondary", className="me-2"),
                        dbc.Button("Redo", id="redo-button", color="secondary", className="me-2"),
                        dbc.Button("Auto Layout", id="auto-layout-button", color="info", className="me-2"),
                    ], className="mt-3")
                ])
            ]),
            node_config_panel,
            dbc.Progress(id="workflow-progress", value=0, className="mt-3"),
        ], width=9)
    ]),
    dcc.Store(id='cytoscape-store'),
    dcc.Store(id='undo-store', data=[]),
    dcc.Store(id='redo-store', data=[]),
])

@callback(
    Output('run-flow-button', 'disabled'),
    Input('cytoscape', 'elements')
)
def validate_workflow(elements):
    if not elements:
        return True
    G = nx.DiGraph()
    for ele in elements:
        if 'source' in ele.get('data', {}) and 'target' in ele.get('data', {}):
            G.add_edge(ele['data']['source'], ele['data']['target'])
    return not nx.is_directed_acyclic_graph(G)

@callback(
    Output('cytoscape', 'elements'),
    Output('undo-store', 'data'),
    Output('redo-store', 'data'),
    Input('undo-button', 'n_clicks'),
    Input('redo-button', 'n_clicks'),
    Input('cytoscape', 'elements'),
    State('undo-store', 'data'),
    State('redo-store', 'data'),
    prevent_initial_call=True
)
def undo_redo(undo_clicks, redo_clicks, current_elements, undo_stack, redo_stack):
    triggered_id = ctx.triggered_id
    if triggered_id == 'undo-button' and undo_stack:
        prev_state = undo_stack.pop()
        redo_stack.append(current_elements)
        return prev_state, undo_stack, redo_stack
    elif triggered_id == 'redo-button' and redo_stack:
        next_state = redo_stack.pop()
        undo_stack.append(current_elements)
        return next_state, undo_stack, redo_stack
    elif triggered_id == 'cytoscape':
        undo_stack.append(current_elements)
        return current_elements, undo_stack, []
    return no_update, no_update, no_update

@callback(
    Output('cytoscape', 'layout'),
    Input('auto-layout-button', 'n_clicks'),
    prevent_initial_call=True
)
def auto_layout(n_clicks):
    return {'name': 'cose'}

@callback(
    Output('workflow-progress', 'value'),
    Input('run-flow-button', 'n_clicks'),
    prevent_initial_call=True
)
def run_workflow(n_clicks):
    # Simulate workflow execution
    import time
    for i in range(101):
        time.sleep(0.05)
        yield i

@callback(
    Output('cytoscape-store', 'data'),
    Input('import-workflow', 'n_clicks'),
    prevent_initial_call=True
)
def import_workflow(n_clicks):
    # Implement file upload and parsing logic here
    # For now, we'll just return a sample workflow
    return json.dumps([
        {'data': {'id': 'node1', 'label': 'Data Source'}},
        {'data': {'id': 'node2', 'label': 'Preprocessing'}},
        {'data': {'source': 'node1', 'target': 'node2'}}
    ])

@callback(
    Output('download', 'data'),
    Input('export-workflow', 'n_clicks'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def export_workflow(n_clicks, elements):
    return dict(content=json.dumps(elements), filename="workflow.json")

# Add new nodes to the cytoscape layout
@callback(
    Output('cytoscape', 'elements', allow_duplicate=True),
    Input({'type': 'add-node', 'index': dash.ALL}, 'n_clicks'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def add_node(n_clicks, elements):
    if not any(n_clicks) or not ctx.triggered_id:
        return no_update
    
    new_node_type = ctx.triggered_id['index']
    new_node = {
        'data': {
            'id': f'node_{len(elements) + 1}',
            'label': new_node_type,
            'type': new_node_type
        },
        'position': {'x': 100, 'y': 100}
    }
    
    return elements + [new_node]

# Connect nodes
@callback(
    Output('cytoscape', 'elements', allow_duplicate=True),
    Input('connect-nodes-button', 'n_clicks'),
    State('cytoscape', 'selectedNodeData'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def connect_nodes(n_clicks, selected_nodes, elements):
    if not n_clicks or len(selected_nodes) != 2:
        return no_update
    
    new_edge = {
        'data': {
            'source': selected_nodes[0]['id'],
            'target': selected_nodes[1]['id'],
            'id': f"edge_{selected_nodes[0]['id']}_{selected_nodes[1]['id']}"
        }
    }
    
    return elements + [new_edge]

# Delete selected nodes and edges
@callback(
    Output('cytoscape', 'elements', allow_duplicate=True),
    Input('delete-selected-button', 'n_clicks'),
    State('cytoscape', 'selectedNodeData'),
    State('cytoscape', 'selectedEdgeData'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def delete_selected(n_clicks, selected_nodes, selected_edges, elements):
    if not n_clicks:
        return no_update
    
    selected_ids = set(node['id'] for node in selected_nodes) | set(edge['id'] for edge in selected_edges)
    updated_elements = [ele for ele in elements if ele['data']['id'] not in selected_ids]
    
    return updated_elements