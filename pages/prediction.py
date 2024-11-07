# pages/prediction.py
from dash import dcc, html, Input, Output, State
import joblib
import pandas as pd 
from config import app
#Importation des librairies 
import joblib
import pandas as pd
from config import app


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
                                    className="header-description",
                                    
                                ),
                            ],
                            className="header",
                            id = "headerprediction"
                        ),
                       
                    ]
                )
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"

    return html.Div([
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

                  
                    # Zone de résultats avec animation
                    html.Div(
                        id="resultats-etiquette", 
                        className="result-container", 
                        children=[
                            html.H4("Résultat de l'étiquette énergétique :"),
                            html.P(id="resultat-etiquette-text", children="Le résultat de l'étiquette s'affichera ici après la prédiction.")
                        ],
                        style={'opacity': 0, 'transition': 'opacity 0.5s ease-in-out'}  # Masquée par défaut avec animation
                    )

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
                        
                        # Type de bâtiment
                        html.Label("Type de bâtiment", htmlFor='type_batiment'),
                        dcc.Dropdown(
                            id='type_batiment', 
                            options=[
                                {'label': 'Maison', 'value': 'Maison'},
                                {'label': 'Appartement', 'value': 'Appartement'},
                                {'label': 'Immeuble', 'value': 'Immeuble'}
                            ], 
                            placeholder='Type de bâtiment'
                        ), 

                          
                        # Hauteur sous plafond en mètres (1 à 5)
                        html.Label("Hauteur sous plafond (mètres)", htmlFor='hauteur_plafond'),
                        dcc.Slider(
                            id='hauteur_plafond', 
                            min=1, 
                            max=5, 
                            step=0.1, 
                            marks={i: str(i) for i in range(1, 6)}, 
                            tooltip={"placement": "bottom", "always_visible": True}, 
                            value=2.5,  # Valeur par défaut
                        ),
                        
                        # Etiquette DPE (A à G)
                        html.Label("Etiquette DPE", htmlFor='etiquette_dpe'),
                        dcc.Dropdown(
                            id='etiquette_dpe', 
                            options=[{'label': label, 'value': label} for label in ['A', 'B', 'C', 'D', 'E', 'F', 'G']], 
                            placeholder='Etiquette DPE'
                        ), 
                        
                        # Année de construction (1731 à 2024)
                        html.Label("Année de construction", htmlFor='annee_construction'),
                        dcc.Dropdown(
                            id='annee_construction', 
                            options=[{'label': str(year), 'value': year} for year in range(1731, 2025)], 
                            placeholder='Année de construction'
                        ), 
                      
                    ]),
                    
                    # Colonne droite
                    html.Div(className="field-group", children=[
                        
                        # Code INSEE (BAN)
                        html.Label("Code INSEE (BAN)", htmlFor='code_insee'),
                        dcc.Input(id='code_insee', type='text', placeholder='Code INSEE (BAN)'), 
                        
                        # Surface habitable en m² (1 à 200, ajustable avec un slider)
                        html.Label("Surface habitable (m²)", htmlFor='surface_habitable'),
                        dcc.Slider(
                            id='surface_habitable', 
                            min=1, 
                            max=200, 
                            step=1, 
                            marks={i: str(i) for i in range(1, 201, 20)}, 
                            tooltip={"placement": "bottom", "always_visible": True}, 
                            value=50,  # Valeur par défaut
                        ), 
                        
                        # Type d'énergie principale pour le chauffage
                        html.Label("Type d'énergie principale chauffage", htmlFor='type_energie'),
                        dcc.Dropdown(
                            id='type_energie', 
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
                        html.Label("Isolation toiture", htmlFor='isolation_toiture'),
                        dcc.Dropdown(
                            id='isolation_toiture', 
                            options=[
                                {'label': 'Non', 'value': 0},
                                {'label': 'Oui', 'value': 1},
                                {'label': 'Inconnue', 'value': 2}
                            ], 
                            placeholder='Isolation toiture'
                        ),

                        # Classe inertie bâtiment
                        html.Label("Classe inertie bâtiment", htmlFor='classe_inertie_batiment'),
                        dcc.Dropdown(
                            id='classe_inertie_batiment', 
                            options=[
                                {'label': 'Légère', 'value': 'Légère'},
                                {'label': 'Moyenne', 'value': 'Moyenne'},
                                {'label': 'Lourde', 'value': 'Lourde'},
                                {'label': 'Très lourde', 'value': 'Très lourde'}
                            ], 
                            placeholder='Classe inertie bâtiment'
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

#callback pour predire l'etiquette 
@app.callback(
    Output("resultat-etiquette-text", "children"),
    Output("resultats-etiquette", "style"),  # Change le style de la zone de résultats
    Input("predict-label-button", "n_clicks"),
    prevent_initial_call=True  # Ne pas déclencher avant un clic
)
def predict_etiquette(n_clicks):
    # Si le bouton n'a pas été cliqué, on ne fait rien
    if n_clicks is None:
        return "", {'opacity': 0, 'transition': 'opacity 0.5s ease-in-out'}

    # Lorsque le bouton est cliqué, on affiche la zone de résultats
    return "Voici la prédiction de l'étiquette énergétique.", {'opacity': 1, 'transition': 'opacity 0.5s ease-in-out'}



# model = joblib.load("./models/pipeline_ml_regression.pkl")
# Callback pour prédire la consommation énergétique
@app.callback(
    Output('resultat-consommation-text', 'children'),
    Input('predict-consumption-button', 'n_clicks'),
    State('type_batiment', 'value'),
    State('hauteur_plafond', 'value'),
    State('etiquette_dpe', 'value'),
    State('annee_construction', 'value'),
    State('code_insee', 'value'),
    State('surface_habitable', 'value'),
    State('type_energie', 'value'),
    State('isolation_toiture', 'value'),
    State('classe_inertie_batiment', 'value')
)
def predict_consumption(n_clicks, type_batiment, hauteur_plafond, etiquette_dpe, annee_construction, code_insee, surface_habitable, type_energie, isolation_toiture, classe_inertie_batiment):
    if n_clicks is None:
        return "Le résultat de la consommation s'affichera ici après la prédiction."
    
    # Vérification des données manquantes
    missing_fields = []
    if not type_batiment:
        missing_fields.append("Type de bâtiment")
    if not hauteur_plafond:
        missing_fields.append("Hauteur sous plafond")
    if not etiquette_dpe:
        missing_fields.append("Etiquette DPE")
    if not annee_construction:
        missing_fields.append("Année de construction")
    if not code_insee:
        missing_fields.append("Code INSEE")
    if not surface_habitable:
        missing_fields.append("Surface habitable")
    if not type_energie:
        missing_fields.append("Type d'énergie principale chauffage")
    if not isolation_toiture:
        missing_fields.append("Isolation toiture")
    if not classe_inertie_batiment:
        missing_fields.append("Classe inertie bâtiment")

    if missing_fields:
        return f"Erreur: Veuillez remplir tous les champs pour obtenir une prédiction. Champs manquants: {', '.join(missing_fields)}"
    
    # Préparation des données pour la prédiction
    data = pd.DataFrame({
        'type_batiment': [type_batiment],
        'hauteur_plafond': [hauteur_plafond],
        'etiquette_dpe': [etiquette_dpe],
        'annee_construction': [annee_construction],
        'code_insee': [code_insee],
        'surface_habitable': [surface_habitable],
        'type_energie': [type_energie],
        'isolation_toiture': [isolation_toiture],
        'classe_inertie_batiment': [classe_inertie_batiment]
    })
    from sklearn.base import BaseEstimator, TransformerMixin
    import category_encoders as ce
    import joblib

    # Transformateur personnalisé pour convertir la colonne isolation toiture en type `str`
    class ConvertToStrTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None):
            return self  # Rien à ajuster
        
        def transform(self, X):
            # Conversion de la colonne en type `str`
            return X.astype(str)
        
    class TargetEncodingTransformer(BaseEstimator, TransformerMixin):
        def __init__(self, cols=None):
            self.cols = cols
            self.encoder = ce.TargetEncoder(cols=self.cols)
        
        def fit(self, X, y):
            self.encoder.fit(X, y)
            return self
        
        def transform(self, X):
            return self.encoder.transform(X)
        print(data)

    # Prédiction
    MODEL = joblib.load('./models/scripts/pipeline_ml_regression.pkl')
    prediction = MODEL.predict(data)[0]


    
    return f"La consommation énergétique estimée est de {prediction:.2f} kWh."