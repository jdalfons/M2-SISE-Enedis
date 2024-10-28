# M2-Enedis

# M2-Enedis

## Architecture du projet 
greentech_dashboard/
├── app.py                     # Script principal pour exécuter l'application Dash
├── assets/                    # Dossier pour les styles CSS, icônes, images, etc.
│   ├── styles.css             # Styles personnalisés pour l'application
├── data/                      # Dossier pour les jeux de données 
│   ├── initial_data.csv       
├── models/                    # Modèles de Machine Learning, notebook et pipelines tout ce qui va conerné les script python
│   ├── model.py               # Code pour entraîner et prédire
│   ├── trained_model.pkl      # Modèle entraîné sauvegardé pour les prédictions
├── pages/                     # Pages de l'application avec différents onglets
│   ├── __init__.py            # Nécessaire pour rendre le dossier importable en tant que package
│   ├── home.py                # Page d'accueil avec introduction et KPIs
│   ├── prediction.py          # Page de prédiction demandé par le client
│   ├── contexte.py            # Page contexte des statistiques et graphiques
│   ├── map.py                 # Page cartographique
├── components/                # Composants réutilisables de Dash
│   ├── navbar.py              # Barre de navigation avec onglets
│   ├── filters.py             # Filtres pour affiner les statistiques et la cartographie(**facultative**)
│   ├── export_button.py       # Bouton d'exportation des graphiques(**facultative**)
├── services/                  # Logique d'intégration de données et API
│   ├── api.py                 # API pour accéder au modèle prédictif
├── requirements.txt           # Liste des packages Python nécessaires
├── README.md                  # Documentation du projet
└── .gitignore                 # Fichiers et dossiers à ignorer par Git
