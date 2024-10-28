# pages/map.py
from dash import html

def render_map(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    return html.Div([
        html.H2("Cartographie des Consommations Énergétiques"),
        html.P("Analysez la consommation énergétique en fonction de la localisation.")
    ],
        className=pagecontent_class,
        id="pageMap"
    )