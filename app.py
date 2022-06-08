import dash
import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.config.suppress_callback_exceptions = True
