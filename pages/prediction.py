# pages/prediction.py
from dash import dcc, html

def render_prediction(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"

    return html.Div([
        html.H2("Prédictions"),
        
        # Composant d'onglets
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
                            dcc.Input(id='text-input-3', type='text', placeholder='Nom du bien'),
                            dcc.Dropdown(id='select-9', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Surface habitable'),
                            dcc.Dropdown(id='select-10', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Nombre de pièces'),
                            dcc.Dropdown(id='select-11', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Type de vitrage'),
                        ]),
                        
                        # Colonne droite
                        html.Div(className="field-group", children=[
                            dcc.Input(id='text-input-4', type='text', placeholder='Adresse'),
                            dcc.Dropdown(id='select-12', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Ventilation'),
                            dcc.Dropdown(id='select-13', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='Climatisation'),
                            dcc.Dropdown(id='select-14', options=[{'label': f'Option {i}', 'value': i} for i in range(1, 6)], placeholder='État de l\'isolation'),
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
