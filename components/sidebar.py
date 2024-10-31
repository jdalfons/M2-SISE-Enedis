# composant sidebar
from dash import html
import dash_bootstrap_components as dbc

def create_sidebar(collapsed):
    sidebar_class = "sidebar collapsed" if collapsed else "sidebar"
    return html.Div(
        [
           html.Div(
                [
                    html.Img(src="/assets/logo.png", className="logo"),
                    html.H2("GreenTech", id="sidebar-title"),
                ],
                className="sidebar-header",
                id="sidebar-header",
            ),
            html.Hr(),
          dbc.Nav(
                [
                    dbc.NavLink([html.I(className="fas fa-home"), html.Span("Home")], href="/", active="exact"),
                    dbc.NavLink([html.I(className="fas fa-chart-line"), html.Span("Prédiction")], href="/prediction", active="exact"),
                    dbc.NavLink([html.I(className="fas fa-map-marker-alt"), html.Span("Map")], href="/map", active="exact"),
                    dbc.NavLink([html.I(className="fas fa-chart-bar"), html.Span("Contexte")], href="/contexte", active="exact"),
                    dbc.NavLink([html.I(className="fas fa-chart-pie"), html.Span("Analytiques")], href="/analytiques", active="exact"),
                ],
                vertical=True,
                pills=True,
                className="sidebar-nav"
            ),

        ],
        className=sidebar_class,
        id="sidebar"
    )
