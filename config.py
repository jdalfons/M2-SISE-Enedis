import dash
import dash_bootstrap_components as dbc

# Constants for paths
PREDICTION_PATH = "/prediction"
MAP_PATH = "/map"
CONTEXTE_PATH = "/contexte"
ANALYTIQUES_PATH = "/analytiques"
HOME_PATH = "/"
DATA = "./data/data_output.csv"

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet"
    }, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"]

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



fields = ['Etiquette_DPE',
    'Type_bâtiment',
    'Coût_chauffage',
    'Année_construction',
    'Surface_habitable_immeuble',
    'Emission_GES_5_usages',
    'Coût_chauffage_dépensier',
    'Conso_5_usages_é_finale',
    'Adresse_brute',
    'Code_postal_(BAN)',
    'Identifiant__BAN',
    'Date_réception_DPE',
    'Adresse_(BAN)',
    'Qualité_isolation_enveloppe',
    'Surface_habitable_logement',
    'Coût_auxiliaires',
    'Type_installation_chauffage_n°1',
    'Type_installation_chauffage',
    'Conso_5_usages/m²_é_finale',
    'Coût_refroidissement',
    'Type_énergie_n°1',
    'Coût_ECS',
    'Coût_total_5_usages',
    'Coût_éclairage'
    ]