from dash import html


def render_home(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    # Zone avec les 4 blocs horizontaux

   


    # Zone de texte avec une colonne pour le texte à gauche et une colonne pour la vidéo à droite
    text_section = html.Div(
        [
            # Colonne de texte à gauche
            html.Div(
                [
                    html.H3("À propos de notre application GreenTech Solutions"),
                    html.P(
                        "L’application web, développée en Dash, vise à prédire la consommation énergétique "
                        "et l’étiquette DPE (Diagnostic de Performance Énergétique) des bâtiments dans le département du Rhône."
                        "L’outil offre une interface interactive pour explorer les données, visualiser des tendances énergétiques,"
                        " et générer des prédictions, répondant ainsi aux besoins des chercheurs, urbanistes et professionnels du bâtiment."
                    ),
                ],
                className="text-section-left"  # Style pour la colonne gauche
            ),

            # Colonne de vidéo à droite
            html.Div(
                [
                    html.Iframe(
                        src="https://www.youtube.com/embed/TH3bm7r2nYE?si=QhjXo3gq4X_Nz8IP",  # Remplacez 'videoID' par l'ID de votre vidéo
                        className="video-section",
                        style={"width": "100%", "height": "100%"}
                    )
                ],
                className="text-section-right"  # Style pour la colonne droite
            ),
        ],
        className="text-video-section"  # Conteneur principal pour les deux colonnes
    )


    stats_section = html.Div(
    [   
        html.Div(
            [
                html.Img(src="/assets/url_photo_juan.jpg", className="stat-photo"),  # Espace pour la photo
                html.P("JUAN", className="stat-value-green", style={"margin": "0", "textAlign": "center"}),
                
            ],
            className="stat-block", style={"animationDelay": "0.2s"}
        ),
        html.Div(
            [
                html.Img(src="/assets/url_photo_pierre.jpg", className="stat-photo"),  # Espace pour la photo
                html.P("PIERRE", className="stat-value-yellow", style={"margin": "0", "textAlign": "center"}),
             
            ],
            className="stat-block", style={"animationDelay": "0.4s"}
        ),
        html.Div(
            [
                html.Img(src="/assets/url_photo_bertrand.jpg", className="stat-photo"),  # Espace pour la photo
                html.P("BERTRAND", className="stat-value-orange", style={"margin": "0", "textAlign": "center"}),
               
            ],
            className="stat-block", style={"animationDelay": "0.6s"}
        ),
        html.Div(
            [
                html.Img(src="/assets/url_photo_souraya.jpeg", className="stat-photo"),  # Espace pour la photo
                html.P("SOURAYA", className="stat-value-red", style={"margin": "0", "textAlign": "center"}),
               
            ],
            className="stat-block", style={"animationDelay": "0.8s"}
        )
    ],
    className="stats-section"
)


    # Assemblage de la page
    return html.Div(
        [
            html.H1("Bienvenue chez GreenTech Solutions", className="main-title"),

            text_section, 
            html.H3("notre équipe", className="title3"),
            stats_section
        ],
        className=pagecontent_class,
        id="pageHome"
    )
