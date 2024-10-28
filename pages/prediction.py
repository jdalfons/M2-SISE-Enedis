# pages/prediction.py
from dash import html

def render_prediction(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    return html.Div([
        html.H2("Prédiction des Consommations Énergétiques"),
        html.P("Sélectionnez les paramètres pour estimer la consommation énergétique d'un bien.")
    ],
        className=pagecontent_class,
        id="pagePrediction"
    )