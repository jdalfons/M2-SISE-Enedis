from dash import html


def render_home(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    # Zone avec les 4 blocs horizontaux

    stats_section = html.Div(
        [
            html.Div(
                [
                    html.P("75%", className="stat-value-green", style={"margin": "0", "textAlign": "center"}),
                    html.Div(
                        [
                            html.I(className="fas fa-bolt", style={"fontSize": "2rem", "color": "#4CAF50"}),  # Icône
                            html.P(
                                "Consommation",
                                style={"margin": "0", "fontWeight": "bold", "textAlign": "left"}
                            )  # Texte
                        ],
                        style={"display": "flex", "alignItems": "center"}
                    )
                ],
                className="stat-block"
            ),
            html.Div(
                [
                    html.P("75%", className="stat-value-yellow", style={"margin": "0", "textAlign": "center"}),
                    html.Div(
                        [
                            html.I(className="fas fa-wind", style={"fontSize": "2rem", "color": "#FFC107"}),
                            html.P(
                                "Énergie renouvelable",
                                style={"margin": "0", "fontWeight": "bold", "textAlign": "left"}
                            )
                        ],
                        style={"display": "flex", "alignItems": "center"}
                    )
                ],
                className="stat-block"
            ),
            html.Div(
                [
                    html.P("30kg", className="stat-value-orange", style={"margin": "0", "textAlign": "center"}),
                    html.Div(
                        [
                            html.I(className="fas fa-cloud", style={"fontSize": "2rem", "color": "#FF8C00"}),
                            html.P(
                                "Émissions CO2",
                                style={"margin": "0", "fontWeight": "bold", "textAlign": "left"}
                            )
                        ],
                        style={"display": "flex", "alignItems": "center"}
                    )

                ],
                className="stat-block"
            ),
            html.Div(
                [
                    html.P("80%", className="stat-value-red", style={"margin": "0", "textAlign": "center"}),
                    html.Div(
                        [
                            html.I(className="fas fa-seedling", style={"fontSize": "2rem", "color": "#FF4B4B"}),
                            html.P(
                                "Impact environnemental",
                                style={"margin": "0", "fontWeight": "bold", "textAlign": "left"}
                            )
                        ],
                        style={"display": "flex", "alignItems": "center"}
                    )
                ],
                className="stat-block"
            )
        ],
        className="stats-section"
    )

    # Zone de texte avec une colonne pour le texte à gauche et une colonne pour la vidéo à droite
    text_section = html.Div(
        [
            # Colonne de texte à gauche
            html.Div(
                [
                    html.H3("À propos de GreenTech Solutions"),
                    html.P(
                        "GreenTech Solutions s'engage à fournir des solutions énergétiques durables et "
                        "à promouvoir l'usage d'énergie propre. Notre mission est de réduire l'empreinte "
                        "carbone et d'améliorer la performance énergétique."
                    ),
                ],
                className="text-section-left"  # Style pour la colonne gauche
            ),

            # Colonne de vidéo à droite
            html.Div(
                [
                    html.Iframe(
                        src="https://www.youtube.com/embed/videoID",  # Remplacez 'videoID' par l'ID de votre vidéo
                        className="video-section",
                        style={"width": "100%", "height": "100%"}
                    )
                ],
                className="text-section-right"  # Style pour la colonne droite
            ),
        ],
        className="text-video-section"  # Conteneur principal pour les deux colonnes
    )

    # Assemblage de la page
    return html.Div(
        [
            html.H1("Bienvenue chez GreenTech Solutions", className="main-title"),
            stats_section,
            text_section
        ],
        className=pagecontent_class,
        id="pageHome"
    )
