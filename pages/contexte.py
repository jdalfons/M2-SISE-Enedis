
# pages/context.py
from dash import html, dcc
from components.kpi import render_kpi
from components.filters import render_radio_button, render_slider, render_checkbox, render_dropdown


def render_contexte(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    
    
   # Section des KPI
    kpi_section = html.Div(
        [
            render_kpi(
                "Logements par Etiquette DPE", # on peut modifier les kpi il faut qu'on se mette d'accord les quels ont veut affichers
                "1200",
                color="linear-gradient(135deg, #4CAF50, #81C784)",  # Vert moderne
                icon_class="fas fa-tags"
            ),
            render_kpi("Date de réception DPE","Moyenne: 2015",color="linear-gradient(135deg, #FFC107, #FFD54F)", icon_class="fas fa-calendar-alt"),
            render_kpi("Surface habitable moyenne","75 m²",color="linear-gradient(135deg, #FF8C00, #FFA726)",icon_class="fas fa-home"),
            render_kpi("Coût moyen de chauffage","300€",color="linear-gradient(135deg, #FF4B4B, #E57373)",icon_class="fas fa-euro-sign"),
        ],
        className="kpi-section"
    )

    

    # Section pour les filtres
    filters_section = html.Div(
        [
            render_radio_button("filter-type-logement", ["Ancien", "Neuf"], label="Type de Logement"),
            render_slider("filter-surface", 0, 200, 10, 100, label="Surface Habitable (m²)"),
            #render_checkbox("filter-DPE", ["D", "E", "F", "G"], label="Etiquette DPE"),
            render_dropdown("filter-type-batiment", ["Appartement", "Maison", "Bureau"], label="Type de Bâtiment", multi=True)
        ],
        className="filter-section"
    )

    # Section pour les visualisations (4 types de graphiques)
    visualizations_section = html.Div(
        [
            html.Div(dcc.Graph(id="histogram-dpe"), className="visualization-card"),
            html.Div(dcc.Graph(id="boxplot-ecs"), className="visualization-card"),
            html.Div(dcc.Graph(id="pie-chart-chauffage"), className="visualization-card"),
            html.Div(dcc.Graph(id="scatterplot-surface"), className="visualization-card")
        ],
        className="visualizations-section"
    )

    # Section pour le tableau des données
    data_table_section = html.Div(
        html.P("Tableau des données (Filtrées):"),
        className="data-table-section"
    )

    return html.Div(
        [
            html.H2("Contexte : Statistiques et Visualisation", className="page-title"),
            kpi_section,
            filters_section,
            visualizations_section,
            data_table_section
        ],
        className=pagecontent_class,
        id="pageContexte"
    )
