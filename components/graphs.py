import plotly.graph_objs as go


def create_graph(title, x, y, y_name="Amplitude", x_name='Time (s)', dash_style=None, name='Trace'):
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='lines', line=dict(dash=dash_style), name=name))
    fig.update_layout(title=title, xaxis_title=x_name, yaxis_title=y_name)
    return fig
