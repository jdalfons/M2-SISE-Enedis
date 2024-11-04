# components/kpi.py
from dash import html

def render_kpi(title, value, color="#4CAF50", icon_class="fas fa-chart-bar"):
    """
    Affiche un KPI avec une icône à gauche et le titre et la valeur empilés et centrés à droite.
    title: Titre du KPI (par ex. "Surface habitable moyenne")
    value: Valeur à afficher (par ex. "75 m²")
    color: Couleur de fond du KPI
    icon_class: Classe CSS de l'icône (par ex. "fas fa-home")
    """
    return html.Div(
        className="kpi-card",
        children=[
            # Icône à gauche
            html.Div(
                className="kpi-icon-container",
                children=html.I(className=icon_class)
            ),
            # Texte et valeur à droite, empilés verticalement et centrés
            html.Div(
                className="kpi-content",
                children=[
                    html.P(title, className="kpi-title"),
                    html.H4(value, className="kpi-value")
                ]
            )
        ],
        style={"background": color}
    )
