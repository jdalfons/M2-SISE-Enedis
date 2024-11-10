# pages/prediction.py
from dash import dcc, html, Input, Output, State
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
                id="headerprediction"
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
                            # Champ Nom du bien
                            html.Label("Nom du bien", htmlFor='nom_du_bien'),
                            dcc.Input(id='nom_du_bien', type='text', placeholder='Nom du bien'),
                            # Champ Année de construction
                            html.Label("Année de construction", htmlFor='annee_construction_label'),
                            dcc.Dropdown(
                                id='annee_construction_label',
                                options=[{'label': str(i), 'value': i} for i in range(1731, 2024)],
                                placeholder='Sélectionner l\'année de construction'
                            ),
                            # Champ Surface habitable en m²
                            html.Label("Surface habitable (m²)", htmlFor='surface_habitable'),
                            dcc.Input(
                                id='surface_habitable',
                                type='number',
                                placeholder='Surface habitable en m²',
                                min=1,
                                max=500,
                                step=1
                            ),
                            # Champ Coût total des 5 usages
                            html.Label("Coût total des 5 usages (€)", htmlFor='coût_total_5_usages'),
                            dcc.Input(
                                id='coût_total_5_usages',
                                type='number',
                                placeholder='Coût total des 5 usages',
                                min=0,
                                step=0.01
                            ),
                            # Champ Coût ECS
                            html.Label("Coût ECS (€)", htmlFor='coût_ECS'),
                            dcc.Input(
                                id='coût_ECS',
                                type='number',
                                placeholder='Coût ECS',
                                min=0,
                                step=0.01
                            )
                        ]),
                        # Colonne droite
                        html.Div(className="field-group", children=[
                            # Champ Coût chauffage
                            html.Label("Coût chauffage (€)", htmlFor='coût_chauffage'),
                            dcc.Input(
                                id='coût_chauffage',
                                type='number',
                                placeholder='Coût chauffage',
                                min=0,
                                step=0.01
                            ),
                            # Champ Coût éclairage
                            html.Label("Coût éclairage (€)", htmlFor='coût_éclairage'),
                            dcc.Input(
                                id='coût_éclairage',
                                type='number',
                                placeholder='Coût éclairage',
                                min=0,
                                step=0.01
                            ),
                            # Champ Coût auxiliaires
                            html.Label("Coût auxiliaires (€)", htmlFor='coût_auxiliaires'),
                            dcc.Input(
                                id='coût_auxiliaires',
                                type='number',
                                placeholder='Coût auxiliaires',
                                min=0,
                                step=0.01
                            ),
                            # Champ Coût refroidissement
                            html.Label("Coût refroidissement (€)", htmlFor='coût_refroidissement'),
                            dcc.Input(
                                id='coût_refroidissement',
                                type='number',
                                placeholder='Coût refroidissement',
                                min=0,
                                step=0.01
                            ),
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
                            # CNom du bien
                            html.Label("Nom du bien", htmlFor='nom_bien'),
                            dcc.Input(id='nom_bien', type='text', placeholder='Ma maison par exemple'),
                            # Type de bâtiment
                            html.Label("Type de bâtiment", htmlFor='type_batiment'),
                            dcc.Dropdown(
                                id='type_batiment',
                                options=[
                                    {'label': 'Maison', 'value': 2},
                                    {'label': 'Appartement', 'value': 0},
                                    {'label': 'Immeuble', 'value': 1}
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
                                options=[
                                    {'label': 'A', 'value': 0},
                                    {'label': 'B', 'value': 1},
                                    {'label': 'C', 'value': 2},
                                    {'label': 'D', 'value': 3},
                                    {'label': 'E', 'value': 4},
                                    {'label': 'F', 'value': 5},
                                    {'label': 'G', 'value': 6}
                                ],
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
                            # Code Postal (BAN)
                            html.Label("Code Postal (BAN)", htmlFor='code_postal'),
                            dcc.Input(id='code_postal', type='text', placeholder='Code Postal (BAN)'),
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
                                    {'label': 'Réseau de Chauffage urbain', 'value': 9},
                                    {'label': 'Gaz naturel', 'value': 7},
                                    {'label': 'Fioul domestique', 'value': 12},
                                    {'label': 'Électricité', 'value': 10},
                                    {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 0},
                                    {'label': 'Bois – Bûches', 'value': 5},
                                    {'label': 'Bois – Plaquettes d’industrie', 'value': 8},
                                    {'label': 'Bois – Plaquettes forestières', 'value': 2},
                                    {'label': 'GPL', 'value': 1},
                                    {'label': 'Propane', 'value': 6},
                                    {'label': 'Charbon', 'value': 3},
                                    {'label': "Électricité d'origine renouvelable utilisée dans le bâtiment", 'value': 4},
                                ],
                                placeholder='Type énergie principale chauffage'
                            ),
                            # Isolation toiture (0 pour non, 1 pour oui)
                            html.Label("Isolation toiture", htmlFor='isolation_toiture'),
                            dcc.Dropdown(
                                id='isolation_toiture',
                                options=[
                                    {'label': 'Non', 'value': 0},
                                    {'label': 'Oui', 'value': 2},
                                    {'label': 'Inconnue', 'value': 1}
                                ],
                                placeholder='Isolation toiture'
                            ),
                            # Classe inertie bâtiment
                            html.Label("Classe inertie bâtiment", htmlFor='classe_inertie_batiment'),
                            dcc.Dropdown(
                                id='classe_inertie_batiment',
                                options=[
                                    {'label': 'Légère', 'value': 1},
                                    {'label': 'Moyenne', 'value': 2},
                                    {'label': 'Lourde', 'value': 0},
                                    {'label': 'Très lourde', 'value': 3}
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
                    ],
                        style={'opacity': 0, 'transition': 'opacity 0.5s ease-in-out'}  # Masquée par défaut avec animation
                    )
                ])
            ]),
        ]),
    ],
        className=pagecontent_class,
        id="pagePrediction"
    )


# callback pour predire l'etiquette
@app.callback(
    Output("resultat-etiquette-text", "children"),
    Output("resultats-etiquette", "style"),  # Change le style de la zone de résultats
    Input("predict-label-button", "n_clicks"),
    State('nom_du_bien', 'value'),
    State('annee_construction_label', 'value'),
    State('surface_habitable', 'value'),
    State('coût_total_5_usages', 'value'),
    State('coût_ECS', 'value'),
    State('coût_chauffage', 'value'),
    State('coût_éclairage', 'value'),
    State('coût_auxiliaires', 'value'),
    State('coût_refroidissement', 'value'),
    prevent_initial_call=True  # Ne pas déclencher avant un clic
)
def predict_etiquette(n_clicks, nom_du_bien, annee_construction_label, surface_habitable, coût_total_5_usages, coût_ECS, coût_chauffage, coût_éclairage, coût_auxiliaires, coût_refroidissement):
    # Si le bouton n'a pas été cliqué, on ne fait rien
    if n_clicks is None:
        return "", {'opacity': 0, 'transition': 'opacity 0.5s ease-in-out'}

    print(n_clicks, nom_du_bien, annee_construction_label, surface_habitable, coût_total_5_usages, coût_ECS, coût_chauffage, coût_éclairage, coût_auxiliaires, coût_refroidissement)
    # Vérification des données manquantes
    missing_fields = []
    if not nom_du_bien:
        missing_fields.append("Nom du bien")
    if not annee_construction_label:
        missing_fields.append("Année de construction")
    if surface_habitable is None or surface_habitable <= 0:
        missing_fields.append("Surface habitable")
    if coût_total_5_usages is None or coût_total_5_usages <= 0:
        missing_fields.append("Coût total des 5 usages")
    if coût_ECS is None or coût_ECS < 0:
        missing_fields.append("Coût ECS")
    if coût_chauffage is None or coût_chauffage < 0:
        missing_fields.append("Coût chauffage")
    if coût_éclairage is None or coût_éclairage < 0:
        missing_fields.append("Coût éclairage")
    if coût_auxiliaires is None or coût_auxiliaires < 0:
        missing_fields.append("Coût auxiliaires")
    if coût_refroidissement is None or coût_refroidissement < 0:
        missing_fields.append("Coût refroidissement")

    if missing_fields:
        return f"Erreur: Veuillez remplir tous les champs pour obtenir une prédiction. Champs manquants: {', '.join(missing_fields)}", {'opacity': 1, 'transition': 'opacity 0.5s ease-in-out'}
    else:
        data = pd.DataFrame({
            'annee_construction': [annee_construction_label],
            'surface_habitable_logement': [surface_habitable],
            'cout_total_5_usages': [coût_total_5_usages],
            'cout_ECS': [coût_ECS],
            'cout_chauffage': [coût_chauffage],
            'cout_eclairage': [coût_éclairage],
            'cout_auxiliaires': [coût_auxiliaires],
            'cout_refroidissement': [coût_refroidissement]
        })
        # Prédiction
        MODEL, encoder = joblib.load('./models/pipeline_ml_classification.pkl')
        prediction = MODEL.predict(data)
        prediction_decoded = encoder.inverse_transform(prediction)
        # Lorsque le bouton est cliqué et que tous les champs sont remplis, on affiche la zone de résultats
        return f"Voici la prédiction de l'étiquette énergétique : {prediction_decoded[0]}", {'opacity': 1, 'transition': 'opacity 0.5s ease-in-out'}


# Callback pour prédire la consommation énergétique
@app.callback(
    Output('resultat-consommation-text', 'children'),
    Output("resultats-consommation", "style"),  # Change le style de la zone de résultats
    Input('predict-consumption-button', 'n_clicks'),
    State('type_batiment', 'value'),
    State('hauteur_plafond', 'value'),
    State('etiquette_dpe', 'value'),
    State('annee_construction', 'value'),
    State('code_postal', 'value'),
    State('surface_habitable', 'value'),
    State('type_energie', 'value'),
    State('isolation_toiture', 'value'),
    State('classe_inertie_batiment', 'value')
)
def predict_consumption(n_clicks, type_batiment, hauteur_plafond, etiquette_dpe, annee_construction, code_postal, surface_habitable, type_energie, isolation_toiture, classe_inertie_batiment):
    if n_clicks is None:
        return "", {'opacity': 0, 'transition': 'opacity 0.5s ease-in-out'}

    # Vérification des données manquantes
    missing_fields = []
    if not type_batiment >= 0:
        missing_fields.append("Type de bâtiment")
    if not hauteur_plafond:
        missing_fields.append("Hauteur sous plafond")
    if not etiquette_dpe >= 0:
        missing_fields.append("Etiquette DPE")
    if not annee_construction:
        missing_fields.append("Année de construction")
    if not code_postal:
        missing_fields.append("Code Postal")
    if not surface_habitable:
        missing_fields.append("Surface habitable")
    if not type_energie > 0:
        missing_fields.append("Type d'énergie principale chauffage")
    if not isolation_toiture > 0:
        missing_fields.append("Isolation toiture")
    if not classe_inertie_batiment > 0:
        missing_fields.append("Classe inertie bâtiment")

    if missing_fields:
        return f"Erreur: Veuillez remplir tous les champs pour obtenir une prédiction. Champs manquants: {', '.join(missing_fields)}", {'opacity': 1, 'transition': 'opacity 0.5s ease-in-out'}

    # Préparation des données pour la prédiction
    data = pd.DataFrame({
        'Type_énergie_principale_chauffage': [type_energie],
        'Hauteur_sous-plafond': [hauteur_plafond],
        'Classe_inertie_bâtiment': [classe_inertie_batiment],
        'Année_construction': [annee_construction],
        'Type_bâtiment': [type_batiment],
        'Surface_habitable_logement': [surface_habitable],
        'Etiquette_DPE': [etiquette_dpe],
        'isolation_toiture': [isolation_toiture],
        'code_postal': [code_postal],
    })

    # Prédiction
    MODEL = joblib.load('./models/pipeline_ml_regression.pkl')
    prediction = MODEL.predict(data)

    return f"La consommation énergétique estimée est de {prediction[0]:.2f} kWh.", {'opacity': 1, 'transition': 'opacity 0.5s ease-in-out'}
