from dash import html, dcc, Input, Output
from dash import dash_table
import pandas as pd
from components.kpi import render_kpi
from components.filters import render_dropdown
from config import app, DATA

# Charger le fichier des données
data_concated = pd.read_csv(DATA)

# Extraire les valeurs uniques pour les filtres
data_concated['Periode_construction'] = data_concated['Année_construction'].map(lambda x: 'avant 1960'  if x < 1960  else '1960-1970' if x < 1970  else '1970-1980' if x < 1980  else '1980-1990' if x < 1990  else '1990-2000' if x < 2000  else '2000-2010' if x < 2010  else '2010-2020' if x < 2010 else 'apres 2020')
periode_construction_options = data_concated['Periode_construction'].unique().tolist()
dpe_options = data_concated['Etiquette_DPE'].unique().tolist()
type_batiment_options = data_concated['Type_bâtiment'].unique().tolist()

def render_contexte(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"

    # Section des KPI
    kpi_section = html.Div(
        [
            render_kpi("Total des logements", f"{data_concated.shape[0]}", color="linear-gradient(135deg, #4CAF50, #81C784)", icon_class="fas fa-tags"),
            render_kpi("Consommation Énergétique Totale Moyenne", f"{round(data_concated['Coût_total_5_usages'].mean(), 2)} €", color="linear-gradient(135deg, #FFC107, #FFD54F)", icon_class="fas fa-calendar-alt"),
            render_kpi("Surface habitable moyenne", f"{round(data_concated['Surface_habitable_logement'].mean(), 2)} m²", color="linear-gradient(135deg, #FF8C00, #FFA726)", icon_class="fas fa-home"),
            render_kpi("Coût moyen de chauffage", f"{round(data_concated['Coût_chauffage'].mean(), 2)} €", color="linear-gradient(135deg, #FF4B4B, #E57373)", icon_class="fas fa-euro-sign"),
        ],
        className="kpi-section"
    )

    # Section pour les filtres
    filters_section = html.Div(
        [
            render_dropdown("filter-periode-construction", periode_construction_options, label="Période de construction", multi=True),
            render_dropdown("filter-DPE", dpe_options, label="Etiquette DPE", multi=True),
            render_dropdown("filter-type-batiment", type_batiment_options, label="Type de Bâtiment", multi=True)
        ],
        className="filter-section"
    )

    # Section pour le tableau des données
    data_table_section = html.Div(
        [
            html.P("Tableau des données :"),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": col, "id": col} for col in data_concated.columns],  # Afficher toutes les colonnes
                page_size=10,  # Nombre de lignes par page
                style_table={'overflowX': 'auto'},  # Permet le défilement horizontal si nécessaire
                filter_action='native',  # Permet le filtrage natif dans le tableau
                sort_action='native',  # Permet le tri natif
                data=data_concated.to_dict('records'),  # Ajoutez les données ici
            ),
        ],
        className="data-table-section"
    )


    return html.Div(
        [
            html.H2("Contexte : Statistiques et Visualisation", className="page-title"),
            kpi_section,
            filters_section,
            data_table_section
        ],
        className=pagecontent_class,
        id="pageContexte"
    )
