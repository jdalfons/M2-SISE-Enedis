"""
This module provides the analytical dashboard for energy consumption.
"""

import pandas as pd
from dash import html, dcc, Input, Output, State
from config import app
import plotly.io as pio
import io
import base64
import dash
import pickle
from sklearn.linear_model import LinearRegression

data_energy = (
    pd.read_csv('./data/data_output.csv', 
                low_memory=False, 
                header=0)
)

# Remove outliers based on Coût_chauffage
q1 = data_energy["Coût_chauffage"].quantile(0.25)
q3 = data_energy["Coût_chauffage"].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

data_energy = data_energy[
    (data_energy["Coût_chauffage"] >= lower_bound) & 
    (data_energy["Coût_chauffage"] <= upper_bound)
]

etiquettes_dpe = data_energy["Etiquette_DPE"].sort_values().unique()

# Train a simple linear regression model
X = pd.get_dummies(data_energy["Etiquette_DPE"])
y = data_energy["Coût_chauffage"]
model = LinearRegression()
model.fit(X, y)

# Save the model to a file
with open('energy_model.pkl', 'wb') as f:
    pickle.dump(model, f)

def render_analytiques(collapsed):
    analytics = html.Div(
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
                                html.Div(
                                    children=[
                                        html.Div(children="Etiquette DPE", className="menu-title"),
                                        dcc.Dropdown(
                                            id="etiquette-dpe-filter",
                                            options=[
                                                {"label": etiquette, "value": etiquette}
                                                for etiquette in etiquettes_dpe
                                            ],
                                            value=list(etiquettes_dpe),
                                            multi=True,
                                            clearable=False,
                                            className="dropdown",
                                        ),
                                    ]
                                ),
                            ],
                            className="menu",
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
                                dcc.Graph(
                                    id="bar-chart",
                                    config={"displayModeBar": False},
                                ),
                            ],
                            className="wrapper",
                        ),
                    ]
                )
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    return html.Div([
        analytics
    ],
        className=pagecontent_class,
        id="PageAnalytics"
    )

@app.callback(
    Output("boxplot-chart", "figure"),
    Input("etiquette-dpe-filter", "value"),
)
def update_charts(etiquette_dpe):
    filtered_data = data_energy[data_energy["Etiquette_DPE"].isin(etiquette_dpe)]
    
    boxplot_figure = {
        "data": [
            {
                "x": filtered_data["Etiquette_DPE"],
                "y": filtered_data["Coût_chauffage"],
                "type": "box",
                "boxpoints": "outliers",
                "name": "Coût_chauffage",
            },
        ],
        "layout": {
            "title": {"text": "Boxplot du Coût du Chauffage selon le Type d'Étiquette DPE (Sans Outliers)", "x": 0.05, "xanchor": "left"},
            "xaxis": {"title": "Étiquette DPE"},
            "yaxis": {"title": "Coût du Chauffage"},
            "colorway": ["#636EFA"],
        },
    }

    return boxplot_figure

@app.callback(
    Output("download-graphs", "data"),
    Input("download-button", "n_clicks"),
    Input("etiquette-dpe-filter", "value"),
    prevent_initial_call=True,
)
def download_graphs(n_clicks, etiquette_dpe):
    ctx = dash.callback_context
    if not ctx.triggered or ctx.triggered[0]['prop_id'].split('.')[0] != 'download-button':
        return dash.no_update

    filtered_data = data_energy[data_energy["Etiquette_DPE"].isin(etiquette_dpe)]
    
    boxplot_figure = {
        "data": [
            {
                "x": filtered_data["Etiquette_DPE"],
                "y": filtered_data["Coût_chauffage"],
                "type": "box",
                "boxpoints": "outliers",
                "name": "Coût_chauffage",
            },
        ],
        "layout": {
            "title": {"text": "Boxplot du Coût du Chauffage selon le Type d'Étiquette DPE (Sans Outliers)", "x": 0.05, "xanchor": "left"},
            "xaxis": {"title": "Étiquette DPE"},
            "yaxis": {"title": "Coût du Chauffage"},
            "colorway": ["#636EFA"],
        },
    }

    fig = pio.to_image(boxplot_figure, format='png')
    buffer = io.BytesIO(fig)
    encoded_image = base64.b64encode(buffer.getvalue()).decode()

    return dict(content=encoded_image, filename="graphs.png", base64=True)

@app.callback(
    Output("bar-chart", "figure"),
    Input("etiquette-dpe-filter", "value"),
)
def update_bar_chart(etiquette_dpe):
    filtered_data = data_energy[data_energy["Etiquette_DPE"].isin(etiquette_dpe)]
    
    bar_chart_figure = {
        "data": [
            {
                "x": filtered_data["Etiquette_DPE"],
                "y": filtered_data["Coût_chauffage"],
                "type": "bar",
                "name": "Coût_chauffage",
            },
        ],
        "layout": {
            "title": {"text": "Bar Chart du Coût du Chauffage selon le Type d'Étiquette DPE (Sans Outliers)", "x": 0.05, "xanchor": "left"},
            "xaxis": {"title": "Étiquette DPE"},
            "yaxis": {"title": "Coût du Chauffage"},
            "colorway": ["#636EFA"],
        },
    }

    return bar_chart_figure
