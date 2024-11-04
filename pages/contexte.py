from dash import html

def render_contexte(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    return html.Div([
        html.H2("Statistiques des Consommations Énergétiques"),
        html.P("Visualisez et analysez les consommations par classe de DPE et région.")
    ],
        className=pagecontent_class,
        id="pageContexte"
    )