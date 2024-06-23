from dash import dcc, html


def create_tabs():
    return html.Div(children=[
        dcc.Tabs(id='tabs', value='modulation', children=[
            dcc.Tab(label='Modulation', value='modulation'),
            dcc.Tab(label='Comparison of Modulations', value='comparison')
        ]),
        html.Div(id='comparison-container', style={'padding': '20px'}),
        dcc.Graph(id='modulated-signal-graph', style={'height': '30vh'}, config={'displayModeBar': False}),
        dcc.Graph(id='transmitted-signal-graph', style={'height': '30vh'}, config={'displayModeBar': False}),
        dcc.Graph(id='demodulated-signal-graph', style={'height': '30vh'}, config={'displayModeBar': False}),
        html.Div(id='table-container', style={'padding': '20px'})
    ], style={'padding': 10, 'flex': 1})
