# components/cytoscape_layout.py
import dash_cytoscape as cyto

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
                'width': 'data(width)',
                'height': 'data(height)',
                'shape': 'data(shape)',
                'background-color': 'data(color)',
                'border-color': 'data(border_color)',
                'border-width': 'data(border_width)',
                'font-size': 'data(font_size)',
            }
        },
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'line-color': 'data(color)',
                'target-arrow-color': 'data(color)',
                'label': 'data(label)',
                'font-size': 'data(font_size)',
            }
        }
    ],
    zoom_range=[0.1, 3],
    pan_zoom_enabled=True,
)