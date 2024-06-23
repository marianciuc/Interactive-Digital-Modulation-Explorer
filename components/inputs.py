from dash import dcc, html


def create_input_section():
    return html.Div(children=[
        html.Br(),
        html.H1("Interactive Digital Modulation Explorer", style={'textAlign': 'center'}),
        html.Img(src='/assets/img.png', style={'width': '50%', 'display': 'block', 'margin': 'auto'}),
        html.Div(
            style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'paddingLeft': '100px',
                   'paddingRight': '100px', 'marginBottom': '20px', 'marginTop': '40px'},
            children=[
                html.Label('Enter the text to be converted to a bitstream', style={'textAlign': 'center'}),
                dcc.Input(value='lorem', type='text', id='text',
                          style={'width': '100%', 'marginBottom': "20px", 'marginTop': "10px"}),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'alignItems': 'center', 'paddingLeft': '100px',
                   'paddingRight': '100px', 'marginBottom': '20px'},
            children=[
                html.Label('W (carrier frequency)', style={'marginRight': '10px'}),
                dcc.Input(id='w-input', value='2', type='number', style={'marginRight': '20px', 'width': '80px'}),
                html.Label('Fs (sampling frequency)', style={'marginRight': '10px'}),
                dcc.Input(id='fs-input', value='16384', type='number', style={'marginRight': '20px', 'width': '100px'}),
                html.Label('Tb (bit duration)', style={'marginRight': '10px'}),
                dcc.Input(id='tb-input', value='0.1', type='number', style={'marginRight': '20px', 'width': '100px'}),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'alignItems': 'center', 'paddingLeft': '100px',
                   'paddingRight': '100px', 'marginBottom': '20px'},
            children=[
                html.Div(
                    style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '20px'},
                    children=[
                        html.Div(
                            style={'width': '300px', 'marginRight': '20px'},
                            children=[
                                html.Label('Select Modulation Type'),
                                dcc.Dropdown(options=[{'label': 'ASK', 'value': 'ASK'},
                                                      {'label': 'PSK', 'value': 'PSK'},
                                                      {'label': 'FSK', 'value': 'FSK'}], value='PSK', id='modulation'),
                            ]
                        ),
                        html.Div(
                            style={'width': '300px', 'marginRight': '20px'},
                            children=[
                                html.Label('Select Noise Type'),
                                dcc.Dropdown(
                                    id='noise-type',
                                    options=[
                                        {'label': 'White Noise', 'value': 'white'},
                                        {'label': 'Gaussian Noise', 'value': 'gaussian'},
                                    ],
                                    value='white',
                                ),
                            ]
                        ),
                        html.Div(
                            style={'width': '300px'},
                            children=[
                                html.Label('Choose an order'),
                                dcc.Dropdown(
                                    id='order-type',
                                    options=[
                                        {'label': 'I + II', 'value': '1'},
                                        {'label': 'II + I', 'value': '2'},
                                    ],
                                    value='1',
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            style={'display': 'flex', 'alignItems': 'center', 'paddingLeft': '100px',
                   'paddingRight': '100px'},
            children=[
                html.Label('Alpha (noise level)', style={'marginRight': '10px'}),
                html.Div(
                    style={'width': '80%', 'marginRight': '20px'},
                    children=[
                        dcc.Slider(
                            id='alpha-slider',
                            min=0,
                            max=1,
                            step=0.01,
                            value=0,
                            marks={i / 10: f'{i / 10:.1f}' for i in range(11)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ]
                ),
                html.Label('Beta (attenuation parameter)', style={'marginRight': '10px'}),
                html.Div(
                    style={'width': '80%'},
                    children=[
                        dcc.Slider(
                            id='beta-slider',
                            min=0,
                            max=10,
                            step=0.1,
                            value=0,
                            marks={i: f'{i}' for i in range(11)},
                            tooltip={"placement": "bottom", "always_visible": True}
                        )
                    ]
                )
            ]
        ),
    ], style={'padding': 10, 'flex': 1})
