import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
<<<<<<< HEAD
from components.sidebar import create_sidebar  # Sidebar importée depuis components
from pages import home, prediction, map, contexte, analytiques  # Importation des pages
from config import (
    app, 
    PREDICTION_PATH, 
    MAP_PATH, 
    CONTEXTE_PATH, 
    ANALYTIQUES_PATH, 
    HOME_PATH)


=======
from components.sidebar import create_sidebar
from pages import home, prediction, map, contexte  

# Initialise l'application
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css']
)
>>>>>>> 6543db007f3e7824edfeb93534e21a5ea1f901d3

# Layout principal
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="sidebar-collapsed", data=False),  
    html.Div(id="sidebar-container", children=create_sidebar(collapsed=False)),
    html.Div(id="page-content")
])

def toggle_sidebar(n_clicks, collapsed):
    """
    Toggle the sidebar collapsed state.
    
    Parameters:
    n_clicks (int): Number of clicks on the sidebar header.
    collapsed (bool): Current collapsed state of the sidebar.
    
    Returns:
    tuple: New sidebar content and collapsed state.
    """
    if n_clicks is None:  # Avoid errors at the beginning
        return create_sidebar(collapsed=False), False

    # Inverse the collapsed state and update the store
    new_collapsed = not collapsed
    return create_sidebar(new_collapsed), new_collapsed

def display_page(pathname, collapsed):
    """
    Display the appropriate page based on the URL pathname.
    
    Parameters:
    pathname (str): The URL pathname.
    collapsed (bool): Current collapsed state of the sidebar.
    
    Returns:
    html.Div: The content of the page.
    """
    if pathname == PREDICTION_PATH:
        return prediction.render_prediction(collapsed=collapsed)
    elif pathname == MAP_PATH:
        return map.map_page(collapsed=collapsed)
    elif pathname == CONTEXTE_PATH:
        return contexte.render_contexte(collapsed=collapsed)
    elif pathname == ANALYTIQUES_PATH:
        return analytiques.render_analytiques(collapsed=collapsed)
    return home.render_home(collapsed=collapsed)

# Callback pour gérer le repliement de la sidebar
app.callback(
    Output("sidebar-container", "children"),
    Output("sidebar-collapsed", "data"),  
    Input("sidebar-header", "n_clicks"),
    State("sidebar-collapsed", "data"),
<<<<<<< HEAD
)(toggle_sidebar)

# Callback pour le contenu de la page avec l'état collapsed 
app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname"), 
     Input("sidebar-collapsed", "data")])(display_page)
=======
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
>>>>>>> 6543db007f3e7824edfeb93534e21a5ea1f901d3

if __name__ == "__main__":
    app.run_server(debug=True)
