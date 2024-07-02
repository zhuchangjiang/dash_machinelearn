import dash
from dash import html, dcc, Input, Output, State, callback, no_update
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import json
import uuid

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])

# 模拟数据源
data_sources = {
    "用户数据": ["用户ID", "年龄", "性别", "购买历史"],
    "商品数据": ["商品ID", "类别", "价格", "库存"],
    "交易数据": ["交易ID", "用户ID", "商品ID", "交易金额", "交易时间"]
}

# 定义组件类别和组件
component_categories = {
    "数据处理": [("数据选择", "fa-table"), ("字段筛选", "fa-filter"), ("连接", "fa-link"), ("聚合", "fa-layer-group")],
    "特征工程": [("缺失值处理", "fa-eraser"), ("标准化", "fa-balance-scale"), ("特征编码", "fa-code")],
    "模型训练": [("线性回归", "fa-chart-line"), ("随机森林", "fa-tree"), ("神经网络", "fa-brain")],
    "模型评估": [("交叉验证", "fa-retweet"), ("混淆矩阵", "fa-th"), ("ROC曲线", "fa-chart-area")]
}

# 创建左侧导航栏和组件列表
sidebar = html.Div([
    html.H4("组件库", className="mb-3 text-primary"),
    html.Hr(),
    dbc.Accordion([
        dbc.AccordionItem(
            [
                dbc.Button(
                    [html.I(className=f"fas {icon} me-2"), component],
                    id={"type": "draggable", "index": f"{category}-{component}"},
                    className="draggable-component mb-2 w-100 text-start",
                    color="light",
                    size="sm"
                ) for component, icon in components
            ],
            title=category
        ) for category, components in component_categories.items()
    ], start_collapsed=True, flush=True)
], className="sidebar bg-light p-3 border-end")

# 创建画布
cytoscape_layout = cyto.Cytoscape(
    id='cytoscape',
    layout={'name': 'preset'},
    style={'width': '100%', 'height': '600px'},
    elements=[],
    stylesheet=[
        {
            'selector': 'node',
            'style': {
                'content': 'data(label)',
                'text-valign': 'center',
                'text-halign': 'center',
                'width': '150px',
                'height': '50px',
                'font-size': '12px',
                'background-color': '#007bff',
                'color': 'white',
                'border-width': '2px',
                'border-color': '#0056b3',
                'shape': 'roundrectangle'
            }
        },
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'target-arrow-color': '#6c757d',
                'line-color': '#6c757d',
                'label': 'data(label)',
                'font-size': '10px'
            }
        },
        {
            'selector': ':selected',
            'style': {
                'background-color': '#28a745',
                'border-color': '#1e7e34'
            }
        }
    ]
)

# 节点配置面板
node_config_panel = dbc.Card([
    dbc.CardHeader("节点配置"),
    dbc.CardBody([
        html.Div(id="node-config-content")
    ])
], id="node-config-panel", className="mt-3")

# 主布局
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(sidebar, width=3, className="p-0"),
        dbc.Col([
            html.H2("机器学习工作流设计器", className="text-center mb-4 text-primary"),
            dbc.Card([
                dbc.CardBody([
                    cytoscape_layout,
                    dbc.ButtonGroup([
                        dbc.Button("连接节点", id="connect-nodes-button", color="primary", className="me-2"),
                        dbc.Button("删除选中", id="delete-selected-button", color="danger", className="me-2"),
                        dbc.Button("运行流程", id="run-flow-button", color="success", className="me-2"),
                        dbc.Button("保存", id="save-state-button", color="info", className="me-2"),
                        dbc.Button("加载", id="load-state-button", color="warning")
                    ], className="mt-3")
                ])
            ]),
            node_config_panel,
            dbc.Card([
                dbc.CardHeader("运行结果"),
                dbc.CardBody(id="results-output")
            ], className="mt-3")
        ], width=9)
    ]),
    dcc.Store(id='cytoscape-store')
], fluid=True, className="mt-3")

# 回调函数：添加节点
@app.callback(
    Output('cytoscape', 'elements'),
    Input({'type': 'draggable', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State('cytoscape', 'elements'),
    State('cytoscape', 'mousePosition')
)
def add_node(n_clicks, elements, mouse_position):
    ctx = dash.callback_context
    if not ctx.triggered:
        return no_update
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    component_id = eval(triggered_id)['index']
    
    new_node = {
        'data': {'id': str(uuid.uuid4()), 'label': component_id.split('-')[1], 'type': component_id.split('-')[0]},
        'position': {'x': mouse_position['x'], 'y': mouse_position['y']} if mouse_position else {'x': 100, 'y': 100}
    }
    
    if elements is None:
        elements = []
    elements.append(new_node)
    
    return elements

# 回调函数：连接节点
@app.callback(
    Output('cytoscape', 'elements', allow_duplicate=True),
    Input('connect-nodes-button', 'n_clicks'),
    State('cytoscape', 'selectedNodeData'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def connect_nodes(n_clicks, selected_nodes, elements):
    if n_clicks is None or len(selected_nodes) != 2:
        return no_update
    
    new_edge = {
        'data': {
            'source': selected_nodes[0]['id'],
            'target': selected_nodes[1]['id'],
            'id': f"edge-{selected_nodes[0]['id']}-{selected_nodes[1]['id']}",
            'label': '连接'
        }
    }
    
    elements.append(new_edge)
    return elements

# 回调函数：删除选中的节点和边
@app.callback(
    Output('cytoscape', 'elements', allow_duplicate=True),
    Input('delete-selected-button', 'n_clicks'),
    State('cytoscape', 'selectedNodeData'),
    State('cytoscape', 'selectedEdgeData'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def delete_selected(n_clicks, selected_nodes, selected_edges, elements):
    if n_clicks is None:
        return no_update
    
    selected_ids = set(node['id'] for node in selected_nodes) | set(edge['id'] for edge in selected_edges)
    elements = [ele for ele in elements if ele['data']['id'] not in selected_ids]
    
    return elements

# 回调函数：更新节点配置面板
@app.callback(
    Output('node-config-content', 'children'),
    Input('cytoscape', 'tapNodeData')
)
def update_node_config(node_data):
    if not node_data:
        return "请选择一个节点进行配置"
    
    node_type = node_data.get('type', '')
    
    if node_type == '数据处理':
        return dbc.Form([
            dbc.FormGroup([
                dbc.Label("选择数据源"),
                dbc.Select(
                    id="data-source-select",
                    options=[{"label": src, "value": src} for src in data_sources.keys()],
                    value=list(data_sources.keys())[0]
                )
            ]),
            dbc.FormGroup([
                dbc.Label("选择字段"),
                dbc.Checklist(
                    id="field-checklist",
                    options=[{"label": field, "value": field} for field in data_sources[list(data_sources.keys())[0]]],
                    value=[]
                )
            ])
        ])
    elif node_type == '特征工程':
        return dbc.Form([
            dbc.FormGroup([
                dbc.Label("处理方法"),
                dbc.Select(
                    id="feature-method-select",
                    options=[
                        {"label": "缺失值填充", "value": "fill_na"},
                        {"label": "标准化", "value": "standardize"},
                        {"label": "独热编码", "value": "one_hot"}
                    ],
                    value="fill_na"
                )
            ])
        ])
    elif node_type == '模型训练':
        return dbc.Form([
            dbc.FormGroup([
                dbc.Label("模型类型"),
                dbc.Select(
                    id="model-type-select",
                    options=[
                        {"label": "线性回归", "value": "linear_regression"},
                        {"label": "随机森林", "value": "random_forest"},
                        {"label": "神经网络", "value": "neural_network"}
                    ],
                    value="linear_regression"
                )
            ]),
            dbc.FormGroup([
                dbc.Label("超参数"),
                dbc.Input(id="hyperparameters-input", type="text", placeholder="输入超参数")
            ])
        ])
    else:
        return f"配置 {node_data['label']} 节点"

# 回调函数：更新字段选择
@app.callback(
    Output('field-checklist', 'options'),
    Input('data-source-select', 'value')
)
def update_field_options(selected_source):
    return [{"label": field, "value": field} for field in data_sources.get(selected_source, [])]

# 回调函数：保存画布状态
@app.callback(
    Output('cytoscape-store', 'data'),
    Input('save-state-button', 'n_clicks'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def save_state(n_clicks, elements):
    if n_clicks is None:
        return no_update
    return json.dumps(elements)

# 回调函数：加载画布状态
@app.callback(
    Output('cytoscape', 'elements', allow_duplicate=True),
    Input('load-state-button', 'n_clicks'),
    State('cytoscape-store', 'data'),
    prevent_initial_call=True
)
def load_state(n_clicks, stored_data):
    if n_clicks is None or stored_data is None:
        return no_update
    return json.loads(stored_data)

# 回调函数：运行流程
@app.callback(
    Output('results-output', 'children'),
    Input('run-flow-button', 'n_clicks'),
    State('cytoscape', 'elements'),
    prevent_initial_call=True
)
def run_flow(n_clicks, elements):
    if n_clicks is None:
        return no_update
    # 这里应该实现实际的流程运行逻辑
    # 现在只是返回一个简单的结果
    return html.Div([
        html.P(f"流程已执行"),
        html.P(f"节点数量: {len([e for e in elements if 'source' not in e['data']])}"),
        html.P(f"连接数量: {len([e for e in elements if 'source' in e['data']])}")
    ])

if __name__ == '__main__':
    app.run_server(debug=True)