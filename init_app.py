# init_app.py
import dash
import dash_bootstrap_components as dbc

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css']

app = dash.Dash(
    __name__,
    title = "GreenTech Solutions",
    external_stylesheets=[
        external_stylesheets,
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'  
    ]
)
app.config.suppress_callback_exceptions = True
server = app.server

