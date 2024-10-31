import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from components.sidebar import create_sidebar  # Sidebar importée depuis components
from pages import home, prediction, map, contexte  # Importation des pages

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    }]


app = dash.Dash(
    __name__,
    title = "GreenAPP : Comprenez votre consommation!,",
    external_stylesheets=[
        external_stylesheets,
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'  
    ]
)

fields = ['Date_réception_DPE',
          'Etiquette_DPE',
          'Coût_chauffage',
          'Surface_habitable_logement',
          'Adresse_(BAN)',
          'Code_postal_(BAN)',
          'Identifiant__BAN']