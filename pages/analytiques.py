import dash
import pandas as pd
from dash import html, dcc, Input, Output, State
from config import app, load_data
import plotly.io as pio
import pickle
from sklearn.linear_model import LinearRegression

data_energy = load_data()
communes = ['All'] + [str(commune) for commune in data_energy['nom_commune'].unique().tolist()]

def get_filtered_data(etiquette_dpe, communes_selected):
    filtered_data = data_energy[data_energy["Etiquette_DPE"].isin(etiquette_dpe)]
    if communes_selected and 'All' not in communes_selected:
        filtered_data = filtered_data[filtered_data['nom_commune'].isin(communes_selected)]
    return filtered_data

def render_analytiques(collapsed):
    etiquettes_dpe = data_energy["Etiquette_DPE"].sort_values().unique()

    # Train a simple linear regression model
    X = pd.get_dummies(data_energy["Etiquette_DPE"])
    y = data_energy["Coût_chauffage"]
    model = LinearRegression()
    model.fit(X, y)

    # Save the model to a file
    with open('energy_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    analytics = html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Img(src="./assets/energy.ico", className="header-emoji"),
                                html.H1(
                                    children="consommation énergétique", className="header-title"
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
                                    ],
                                ),
                                html.Div(
                                    children=[
                                        html.Div(children="Commune", className="menu-title"),
                                       dcc.Dropdown(
                                            id='commune-filter',
                                            options=[{'label': commune, 'value': commune} for commune in communes],
                                            value=['Lyon 8e Arrondissement'],
                                            placeholder="Sélectionnez une commune",
                                            multi=True
                                        ),
                                    ]
                                ),
                            ],
                            className="menu",
                        ),
                        
                        html.Div(
                            children=[
                                dcc.Download(id="download-graphs"),
                                dcc.Graph(
                                    id="boxplot-chart",
                                    config={"displayModeBar": True},
                                ),
                                dcc.Graph(
                                    id="bar-chart",
                                    config={"displayModeBar": True},
                                ),
                                dcc.Graph(
                                    id="pie-chart",
                                    config={"displayModeBar": True},
                                ),
                                dcc.Graph(
                                    id="scatter-chart",
                                    config={"displayModeBar": True},
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
    [Output("boxplot-chart", "figure"), 
     Output("bar-chart", "figure"), 
     Output("pie-chart", "figure"),
     Output("scatter-chart", "figure")],
    [Input("etiquette-dpe-filter", "value"),
     Input("commune-filter", "value")]
)
def update_charts(etiquette_dpe, communes_selected):
    filtered_data = get_filtered_data(tuple(etiquette_dpe), tuple(communes_selected))
    
    colors = {
        "A": "#009639",
        "B": "#34A853",
        "C": "#A2C317",
        "D": "#FFD600",
        "E": "#F39C12",
        "F": "#EB6C2A",
        "G": "#E01E27"
    }

    boxplot_figure = {
        "data": [
            {
                "x": filtered_data[filtered_data["Etiquette_DPE"] == etiquette]["Etiquette_DPE"],
                "y": filtered_data[filtered_data["Etiquette_DPE"] == etiquette]["Coût_chauffage"],
                "type": "box",
                "boxpoints": "outliers",
                "name": etiquette,
                "marker": {"color": colors[etiquette]},
            }
            for etiquette in filtered_data["Etiquette_DPE"].unique()
        ],
        "layout": {
            "title": {"text": "Boxplot du Coût du Chauffage selon le Type d'Étiquette DPE (Sans Outliers)", "x": 0.05, "xanchor": "left"},
            "xaxis": {"title": "Étiquette DPE"},
            "yaxis": {"title": "Coût du Chauffage"},
        },
    }

    bar_chart_figure = {
        "data": [
            {
                "x": filtered_data["Periode_construction"],
                "y": filtered_data[filtered_data["Etiquette_DPE"] == etiquette]["Coût_chauffage"],
                "type": "bar",
                "name": etiquette,
                "marker": {"color": colors[etiquette]},
            }
            for etiquette in filtered_data["Etiquette_DPE"].unique()
        ],
        "layout": {
            "title": {"text": "Bar Chart du Coût du Chauffage selon le Type d'Étiquette DPE (Sans Outliers)", "x": 0.05, "xanchor": "left"},
            "xaxis": {"title": "Periode_construction"},
            "yaxis": {"title": "Coût du Chauffage"},
            "barmode": "stack",
        },
    }
    
    energy_counts = filtered_data['Type_énergie_principale_chauffage'].value_counts()
        
    pie_chart_figure = {
            "data": [
                {
                    "values": energy_counts.values,
                    "labels": energy_counts.index,
                    "type": "pie",
                    "textinfo": "label+percent",
                    "insidetextorientation": "radial",
                },
            ],
            "layout": {
                "title": {"text": "Répartition des types d'énergie principaux", "x": 0.5, "xanchor": "center"},
            },
        }

    scatter_chart_figure = {
        "data": [
            {
                "x": filtered_data[filtered_data["Etiquette_DPE"] == etiquette]["Coût_chauffage"],
                "y": filtered_data[filtered_data["Etiquette_DPE"] == etiquette]["Conso_5_usages_é_finale"],
                "mode": "markers",
                "name": etiquette,
            }
            for etiquette in filtered_data["Etiquette_DPE"].unique()
        ],
        "layout": {
            "title": {"text": "Scatter Plot de la Consommation Énergétique vs Coût du Chauffage par Étiquette DPE", "x": 0.05, "xanchor": "left"},
            "xaxis": {"title": "Coût du Chauffage"},
            "yaxis": {"title": "Consommation Énergétique"},
            "colorway": ["#009639", "#34A853", "#A2C317", "#FFD600", "#F39C12", "#EB6C2A", "#E01E27"],
        },
    }

    return boxplot_figure, bar_chart_figure, pie_chart_figure, scatter_chart_figure
