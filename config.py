"""
Configuration file for the GreenTech Solutions Dash application.
"""

import os
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from flask import Flask

# Constants for local paths location
DATA_DIR = 'data'
ADDRESSES_FILE = os.path.join(DATA_DIR, 'adresses-69.csv')
ENERGY_DATA_FILE = os.path.join(DATA_DIR, 'data_output.csv')

MAP_PATH = "/map"
HOME_PATH = "/"
PREDICTION_PATH = "/prediction"
CONTEXTE_PATH = "/contexte"
ANALYTIQUES_PATH = "/analytiques"

# DATASET = (
#     "https://media.githubusercontent.com/media/jdalfons/"
#     "M2-SISE-Enedis/refs/heads/main/datasets/DPE_Enedis_69.csv"
# )
DATASET = "datasets/DPE_Enedis_69.csv"
REG_MODEL_PATH = "models/pipeline_ml_regression.pkl"

def load_data():
    """
    Load data from the dataset URL.
    """
    data = pd.read_csv(DATASET, sep=';', low_memory=False)
    return data

app = Flask(__name__)

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet"
    },
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
]
app = dash.Dash(
    __name__,
    title="GreenTech Solutions",
    external_stylesheets=[
        external_stylesheets,
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
    ]
)
app.config.suppress_callback_exceptions = True
server = app.serverserver = app.serverserver = app.server