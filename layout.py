from dash import html
from components.inputs import create_input_section
from components.tabs import create_tabs


def create_layout():
    return html.Div([
        create_input_section(),
        html.Div(id='table-container-params', style={'padding': '20px'}),
        create_tabs(),
        html.Footer("This work was completed by a student of ZUT, Vladimir Marianiuc.", style={'textAlign': 'center', 'padding': '20px'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'fontFamily': 'Arial, sans-serif'})
