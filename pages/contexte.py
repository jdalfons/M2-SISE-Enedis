from dash import html, dcc, Input, Output
from dash import dash_table
import pandas as pd
from components.kpi import render_kpi
from components.filters import render_dropdown
from config import app, load_data

data_concated = load_data()

periode_construction_options = data_concated['Periode_construction'].unique().tolist()
dpe_options = data_concated['Etiquette_DPE'].unique().tolist()
type_batiment_options = data_concated['Type_bâtiment'].unique().tolist()

def render_contexte(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"

    # KPI Section
    kpi_section = html.Div(
        [
            render_kpi(
                "Total des logements",
                f"{data_concated.shape[0]}",
                color="linear-gradient(135deg, #4CAF50, #81C784)",
                icon_class="fas fa-tags",
            ),
            render_kpi(
                "Consommation Énergétique Totale Moyenne",
                f"{round(data_concated['Coût_total_5_usages'].mean(), 2)} €",
                color="linear-gradient(135deg, #FFC107, #FFD54F)",
                icon_class="fas fa-calendar-alt"
            ),
            render_kpi(
                "Surface habitable moyenne",
                f"{round(data_concated['Surface_habitable_logement'].mean(), 2)} m²",
                color="linear-gradient(135deg, #FF8C00, #FFA726)",
                icon_class="fas fa-home"
            ),
            render_kpi(
                "Coût moyen de chauffage",
                f"{round(data_concated['Coût_chauffage'].mean(), 2)} €",
                color="linear-gradient(135deg, #FF4B4B, #E57373)",
                icon_class="fas fa-euro-sign"
            ),
        ],
        className="kpi-section"
    )

    # Filters Section
    filters_section = html.Div(
        [
            html.H3("Filtres rapides :"),

            # Conteneur des filtres avec une disposition flex
            html.Div(
                [
                    render_dropdown(
                        "filter-periode-construction",
                        periode_construction_options,
                        label="Période de construction",
                        multi=True
                    ),
                    render_dropdown(
                        "filter-DPE",
                        dpe_options,
                        label="Etiquette DPE",
                        multi=True
                    ),
                    render_dropdown(
                        "filter-type-batiment",
                        type_batiment_options,
                        label="Type de Bâtiment",
                        multi=True
                    ),
                    # Ajoutez un bouton si nécessaire
                    # html.Button("Appliquer les filtres", id="apply-filters-button", className="apply-filters-button")
                ],
                className="filters-container"
            ),
        ],
        className="filter-section"
    )

    # Data Table Section avec export CSV
    data_table_section = html.Div(
        [
            html.H3("Tableau des données :"),

            # Bouton d'export CSV
            html.Div(
                html.Button("Exporter en CSV", id="export-csv-button", className="export-button"),
                className="export-button-container"
            ),

            # Composant DataTable
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": col, "id": col} for col in data_concated.columns],
                page_size=10,
                style_table={'overflowX': 'auto'},
                filter_action='native',
                sort_action='native',
                data=data_concated.head(10).to_dict('records'),  # Charge initialement les 10 premières lignes

                # Style pour les cellules, en-têtes, et lignes alternées
                style_data={
                    'backgroundColor': '#f3f3f3',
                    'color': '#333',
                    'border': '1px solid #ddd',
                },
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': '#fafafa'},
                ],
                style_header={
                    'backgroundColor': '#527ead',
                    'fontWeight': 'bold',
                    'color': 'white',
                    'border': '1px solid #ddd',
                },
                style_cell={
                    'padding': '10px',
                    'textAlign': 'left',
                    'minWidth': '100px',
                    'width': '150px',
                    'maxWidth': '300px',
                    'whiteSpace': 'normal',
                }
            ),

            # Téléchargement du fichier CSV
            dcc.Download(id="download-data-csv")
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


# Callback pour exporter le CSV
@app.callback(
    Output("download-data-csv", "data"),
    Input("export-csv-button", "n_clicks"),
    prevent_initial_call=True,
)
def export_data_as_csv(n_clicks):
    # Convertir les données en CSV
    return dcc.send_data_frame(data_concated.to_csv, "data_export.csv")


@app.callback(
    Output('data-table', 'data'),
    # Input('apply-filters-button', 'n_clicks'),
    [
        Input('filter-periode-construction', 'value'),
        Input('filter-DPE', 'value'),
        Input('filter-type-batiment', 'value')
    ]
)
def update_table(selected_periode, selected_dpe, selected_type_batiment):
    filtered_data = data_concated

    if selected_periode:
        filtered_data = filtered_data[filtered_data['Periode_construction'].isin(selected_periode)]
    if selected_dpe:
        filtered_data = filtered_data[filtered_data['Etiquette_DPE'].isin(selected_dpe)]
    if selected_type_batiment:
        filtered_data = filtered_data[filtered_data['Type_bâtiment'].isin(selected_type_batiment)]

    return filtered_data.to_dict('records')
