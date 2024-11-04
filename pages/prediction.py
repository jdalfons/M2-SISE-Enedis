# pages/prediction.py
import pandas as pd
from dash import html, dcc, Input, Output
from init_app import app
import plotly.io as pio
import io
import base64
import dash

def render_prediction(collapsed):
    predictions = html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Img(src="./assets/energy.ico", className="header-emoji"),
                                html.H1(
                                    children="Comsomation Energetique", className="header-title"
                                ),
                                html.P(
                                    children=(
                                        "Analyse de consommation énergétique "
                                        " entre les périodes de 2021 et 2023"
                                    ),
                                    className="header-description",
                                ),
                            ],
                            className="header",
                        ),
                        html.Div(
                            children=[
                                html.Button(
                                    "Download Graphs", 
                                    id="download-button", 
                                    style={
                                        "background-color": "#0B9ED9", 
                                        "color": "white", 
                                        "margin": "0 auto", 
                                        "display": "block",
                                        "border-radius": "5px",
                                        "padding": "10px 20px",
                                        "margin-top": "20px",
                                        "font-size": "16px",
                                        "margin-bottom": "20px",
                                    }
                                ),
                                dcc.Download(id="download-graphs"),
                                dcc.Graph(
                                    id="boxplot-chart",
                                    config={"displayModeBar": False},
                                ),
                            ],
                            className="wrapper",
                        ),
                    ]
                )
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    return html.Div([
        predictions,
    ],
        className=pagecontent_class,
        id="PageAnalytics"
    )