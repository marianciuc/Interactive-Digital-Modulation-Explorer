import os
import dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Data Transmission"
app.layout = create_layout()

register_callbacks(app)
server = app.server

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=False,  host='0.0.0.0', port=port)
