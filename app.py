import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar
from pages import home, prediction, map, contexte  

# Initialise l'application
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css']
)

# Layout principal
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="sidebar-collapsed", data=False),  
    html.Div(id="sidebar-container", children=create_sidebar(collapsed=False)),
    html.Div(id="page-content")
])

# Callback pour gérer le repliement de la sidebar
@app.callback(
    Output("sidebar-container", "children"),
    Output("sidebar-collapsed", "data"),  
    Input("sidebar-header", "n_clicks"),
    State("sidebar-collapsed", "data"),
)
def toggle_sidebar(n_clicks, collapsed):
    if n_clicks is None:  # Évitez les erreurs au début
        return create_sidebar(collapsed=False), False

    new_collapsed = not collapsed
    return create_sidebar(new_collapsed), new_collapsed

# Callback pour le contenu de la page avec l'état collapsed 
@app.callback(Output("page-content", "children"), [Input("url", "pathname"), Input("sidebar-collapsed", "data")])
def display_page(pathname, collapsed):
    if pathname == "/prediction":
        return prediction.render_prediction(collapsed=collapsed)
    elif pathname == "/map":
        return map.render_map(collapsed=collapsed)
    elif pathname == "/contexte":
        return contexte.render_contexte(collapsed=collapsed)  # Appeler la fonction qui rend la page de contexte
    return home.render_home(collapsed=collapsed)

if __name__ == "__main__":
    app.run_server(debug=True)
