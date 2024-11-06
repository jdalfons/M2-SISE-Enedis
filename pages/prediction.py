# pages/prediction.py
from dash import dcc, html, Input, Output, State
import joblib
import pandas as pd
from config import app

# chargement du modele 

def render_prediction(collapsed):
    title_predictions = html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Img(src="./assets/energy.ico", className="header-emoji"),
                                html.H1(
                                    children="Prédictions", className="header-title"
                                ),
                                html.P(
                                    children=(
                                        "Prédictions de la consommation énergétique "
                                        " et etiquette DPE sur le Rhône"
                                    ),
                                    className="header-description" ,
                                ),
                            ],
                            className="header",
                        ),
                       
                    ]
                )
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"

    return html.Div([
        #html.H2("Prédictions"),
        
        # Composant d'onglets
        title_predictions,
        
        dcc.Tabs([
            # Onglet pour prédire les étiquettes
            dcc.Tab(label="Prédiction des Étiquettes", children=[
                html.Div([
                    html.P("Sélectionnez les paramètres pour estimer l'étiquette énergétique du bien."),
                    
                    # Conteneur des champs
                    html.Div(className="fields-container", children=[
                        # Colonne gauche
                        html.Div(className="field-group", children=[
                            dcc.Input(id='text-input-1', type='text', placeholder='Nom du bien'),
                            dcc.Dropdown(id='select-1', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Type de bien'),
                            dcc.Dropdown(id='select-2', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Année de construction'),
                            dcc.Dropdown(id='select-3', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Matériaux de construction'),
                        ]),
                        
                        # Colonne droite
                        html.Div(className="field-group", children=[
                            dcc.Input(id='text-input-2', type='text', placeholder='Adresse'),
                            dcc.Dropdown(id='select-4', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Isolation'),
                            dcc.Dropdown(id='select-5', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Type de chauffage'),
                            dcc.Dropdown(id='select-6', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Énergie utilisée'),
                        ]),
                    ]),

                    # Conteneur du bouton centré
                    html.Div(className="predict-button-container", children=[
                        html.Button('Prédire l\'étiquette', id='predict-label-button', className="predict-button")
                    ]),

                    # Zone de résultats
                    html.Div(id="resultats-etiquette", className="result-container", children=[
                        html.H4("Résultat de l'étiquette énergétique :"),
                        html.P(id="resultat-etiquette-text", children="Le résultat de l'étiquette s'affichera ici après la prédiction.")
                    ])
                ])
            ]),


            # Onglet pour prédire la consommation énergétique
            dcc.Tab(label="Prédiction de la Consommation Énergétique", children=[
                html.Div([
                    html.P("Sélectionnez les paramètres pour estimer la consommation énergétique d'un bien."),
                    
                # Conteneur des champs
                html.Div(className="fields-container", children=[
                    # Colonne gauche
                    html.Div(className="field-group", children=[
                        
                        # Nom du bien
                        html.Label("Nom du bien", htmlFor='text-input-3'),
                        dcc.Input(id='text-input-3', type='text', placeholder='Nom du bien'), 

                          
                        # Hauteur sous plafond en mètres (1 à 5)
                        html.Label("Hauteur sous plafond (mètres)", htmlFor='select-11'),
                        dcc.Slider(
                            id='select-11', 
                            min=1, 
                            max=5, 
                            step=0.1, 
                            marks={i: str(i) for i in range(1, 6)}, 
                            tooltip={"placement": "bottom", "always_visible": True}, 
                            value=2.5,  # Valeur par défaut
                        ),
                        
                        # Etiquette DPE (A à G)
                        html.Label("Etiquette DPE", htmlFor='select-9'),
                        dcc.Dropdown(
                            id='select-9', 
                            options=[{'label': label, 'value': label} for label in ['A', 'B', 'C', 'D', 'E', 'F', 'G']], 
                            placeholder='Etiquette DPE'
                        ), 
                        
                        # Année de construction (1731 à 2024)
                        html.Label("Année de construction", htmlFor='select-10'),
                        dcc.Dropdown(
                            id='select-10', 
                            options=[{'label': str(year), 'value': year} for year in range(1731, 2025)], 
                            placeholder='Année de construction'
                        ), 
                      
                    ]),
                    
                    # Colonne droite
                    html.Div(className="field-group", children=[
                        
                        # Code INSEE (BAN)
                        html.Label("Code INSEE (BAN)", htmlFor='text-input-4'),
                        dcc.Input(id='text-input-4', type='text', placeholder='Code INSEE (BAN)'), 
                        
                        # Surface habitable en m² (1 à 200, ajustable avec un slider)
                        html.Label("Surface habitable (m²)", htmlFor='select-12'),
                        dcc.Slider(
                            id='select-12', 
                            min=1, 
                            max=200, 
                            step=1, 
                            marks={i: str(i) for i in range(1, 201, 20)}, 
                            tooltip={"placement": "bottom", "always_visible": True}, 
                            value=50,  # Valeur par défaut
                        ), 
                        
                        # Type d'énergie principale pour le chauffage
                        html.Label("Type d'énergie principale chauffage", htmlFor='select-13'),
                        dcc.Dropdown(
                            id='select-13', 
                            options=[
                                {'label': 'Réseau de Chauffage urbain', 'value': 'Réseau de Chauffage urbain'},
                                {'label': 'Gaz naturel', 'value': 'Gaz naturel'},
                                {'label': 'Fioul domestique', 'value': 'Fioul domestique'},
                                {'label': 'Électricité', 'value': 'Électricité'},
                                {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 'Bois – Granulés (pellets) ou briquettes'},
                                {'label': 'Bois – Bûches', 'value': 'Bois – Bûches'},
                                {'label': 'Bois – Plaquettes d’industrie', 'value': 'Bois – Plaquettes d’industrie'},
                                {'label': 'GPL', 'value': 'GPL'},
                                {'label': 'Propane', 'value': 'Propane'},
                                {'label': 'Charbon', 'value': 'Charbon'},
                                {'label': 'Bois – Plaquettes forestières', 'value': 'Bois – Plaquettes forestières'},
                                {'label': 'Butane', 'value': 'Butane'},
                                {'label': "Électricité d'origine renouvelable utilisée dans le bâtiment", 'value': "Électricité d'origine renouvelable utilisée dans le bâtiment"},
                            ], 
                            placeholder='Type énergie principale chauffage'
                        ),

                        # Isolation toiture (0 pour non, 1 pour oui)
                        html.Label("Isolation toiture", htmlFor='select-14'),
                        dcc.Dropdown(
                            id='select-14', 
                            options=[
                                {'label': 'Non', 'value': 0},
                                {'label': 'Oui', 'value': 1}
                            ], 
                            placeholder='Isolation toiture'
                        ),
                    ]),
                ]),


                    # Conteneur du bouton centré
                    html.Div(className="predict-button-container", children=[
                        html.Button('Prédire la consommation', id='predict-consumption-button', className="predict-button")
                    ]),

                    # Zone de résultats
                    html.Div(id="resultats-consommation", className="result-container", children=[
                        html.H4("Résultat de la consommation énergétique :"),
                        html.P(id="resultat-consommation-text", children="Le résultat de la consommation s'affichera ici après la prédiction.")
                    ])
                ])
            ]),
        ]),

    ],
        className=pagecontent_class,
        id="pagePrediction"
    ) 


# model = joblib.load("./models/pipeline_ml_regression.pkl")
# Callback pour prédire la consommation énergétique
@app.callback(
    Output('resultat-consommation-text', 'children'),
    Input('predict-consumption-button', 'n_clicks'),
    State('text-input-3', 'value'),
    State('select-11', 'value'),
    State('select-9', 'value'),
    State('select-10', 'value'),
    State('text-input-4', 'value'),
    State('select-12', 'value'),
    State('select-13', 'value'),
    State('select-14', 'value')
)
def predict_consumption(n_clicks, nom_bien, hauteur_plafond, etiquette_dpe, annee_construction, code_insee, surface_habitable, type_energie, isolation_toiture):
    if n_clicks is None:
        return "Le résultat de la consommation s'affichera ici après la prédiction."
    
    # Préparation des données pour la prédiction
    data = pd.DataFrame({
        'nom_bien': [nom_bien],
        'hauteur_plafond': [hauteur_plafond],
        'etiquette_dpe': [etiquette_dpe],
        'annee_construction': [annee_construction],
        'code_insee': [code_insee],
        'surface_habitable': [surface_habitable],
        'type_energie': [type_energie],
        'isolation_toiture': [isolation_toiture]
    })
    
    # Chargement du modèle
    model = joblib.load("./models/pipeline_ml_regression.pkl")
    
    # Prédiction
    prediction = model.predict(data)[0]
    
    return f"La consommation énergétique estimée est de {prediction:.2f} kWh."