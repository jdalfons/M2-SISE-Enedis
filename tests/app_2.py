from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define el estilo del menú lateral y el contenido principal
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "200px",
    "padding": "20px",
    "background-color": "#f8f9fa",
    "transition": "left 0.3s",
}

SIDEBAR_HIDDEN_STYLE = {
    **SIDEBAR_STYLE,
    "left": "-200px",
}

CONTENT_STYLE = {
    "margin-left": "220px",
    "padding": "20px",
    "transition": "margin-left 0.3s",
}

CONTENT_EXPANDED_STYLE = {
    **CONTENT_STYLE,
    "margin-left": "20px",
}

# Definición del menú lateral con enlaces para cada página
sidebar = html.Div(
    [
        html.H2("Menú", className="display-4"),
        html.Hr(),
        html.P("Navegación", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Página 1", href="/page-1", id="page-1-link"),
                dbc.NavLink("Página 2", href="/page-2", id="page-2-link"),
                dbc.NavLink("Página 3", href="/page-3", id="page-3-link"),
                dbc.NavLink("Página 4", href="/page-4", id="page-4-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

# Botón para desplegar y plegar el menú lateral
toggle_button = dbc.Button("Toggle Menu", id="toggle-button", n_clicks=0)

# Contenido principal que se actualizará dinámicamente
content = html.Div(id="page-content", style=CONTENT_STYLE)

# Disposición general de la aplicación
app.layout = html.Div([dcc.Location(id="url"), toggle_button, sidebar, content])

# Callbacks para actualizar el contenido según la página seleccionada
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Redirige a la página 1 por defecto
        return True, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/page-1":
        return html.H3("Contenido de la Página 1")
    elif pathname == "/page-2":
        return html.H3("Contenido de la Página 2")
    elif pathname == "/page-3":
        return html.H3("Contenido de la Página 3")
    elif pathname == "/page-4":
        return html.H3("Contenido de la Página 4")
    # Página no encontrada
    return html.H3("404: Página no encontrada")

@app.callback(
    [Output("sidebar", "style"), Output("page-content", "style")],
    [Input("toggle-button", "n_clicks")],
    [State("sidebar", "style"), State("page-content", "style")]
)
def toggle_sidebar(n_clicks, sidebar_style, content_style):
    if n_clicks % 2 == 1:
        return SIDEBAR_HIDDEN_STYLE, CONTENT_EXPANDED_STYLE
    else:
        return SIDEBAR_STYLE, CONTENT_STYLE

if __name__ == "__main__":
    app.run_server(debug=True)
