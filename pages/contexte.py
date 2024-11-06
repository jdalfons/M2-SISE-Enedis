from dash import html, dcc, Input, Output
from dash import dash_table
import pandas as pd
from components.kpi import render_kpi
from components.filters import render_dropdown
from config import app, DATA
import flask_caching

# Initialize cache
cache = flask_caching.Cache(app.server, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

# Load data and cache it
@cache.memoize()
def load_data():
    data = pd.read_csv(DATA)
    data['Periode_construction'] = data['Année_construction'].map(
    lambda x: 'avant 1960' if x < 1960 else
              '1960-1970' if x < 1970 else
              '1970-1980' if x < 1980 else
              '1980-1990' if x < 1990 else
              '1990-2000' if x < 2000 else
              '2000-2010' if x < 2010 else
              '2010-2020' if x < 2020 else
              'apres 2020'
              )
    # Downsample the data to reduce load
    data = data.groupby('Periode_construction').sample(frac=0.1, random_state=1)  # Adjust the fraction as needed
    return data

data_concated = load_data()

periode_construction_options = data_concated['Periode_construction'].unique().tolist()
dpe_options = data_concated['Etiquette_DPE'].unique().tolist()
type_batiment_options = data_concated['Type_bâtiment'].unique().tolist()

def render_contexte(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"

    # KPI Section
    kpi_section = html.Div(
        [
            render_kpi("Total des logements", f"{data_concated.shape[0]}", color="linear-gradient(135deg, #4CAF50, #81C784)", icon_class="fas fa-tags"),
            render_kpi("Consommation Énergétique Totale Moyenne", f"{round(data_concated['Coût_total_5_usages'].mean(), 2)} €", color="linear-gradient(135deg, #FFC107, #FFD54F)", icon_class="fas fa-calendar-alt"),
            render_kpi("Surface habitable moyenne", f"{round(data_concated['Surface_habitable_logement'].mean(), 2)} m²", color="linear-gradient(135deg, #FF8C00, #FFA726)", icon_class="fas fa-home"),
            render_kpi("Coût moyen de chauffage", f"{round(data_concated['Coût_chauffage'].mean(), 2)} €", color="linear-gradient(135deg, #FF4B4B, #E57373)", icon_class="fas fa-euro-sign"),
        ],
        className="kpi-section"
    )

    # Filters Section
    filters_section = html.Div(
        [
            render_dropdown("filter-periode-construction", periode_construction_options, label="Période de construction", multi=True),
            render_dropdown("filter-DPE", dpe_options, label="Etiquette DPE", multi=True),
            render_dropdown("filter-type-batiment", type_batiment_options, label="Type de Bâtiment", multi=True),
            # html.Button("Appliquer les filtres", id="apply-filters-button", className="apply-filters-button")
        ],
        className="filter-section"
    )

    # Data Table Section
    data_table_section = html.Div(
        [
            html.P("Tableau des données :"),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": col, "id": col} for col in data_concated.columns],
                page_size=10,
                style_table={'overflowX': 'auto'},
                filter_action='native',
                sort_action='native',
                data=data_concated.head(10).to_dict('records'),  # Load only the first 10 rows initially
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

@app.callback(
    Output('data-table', 'data'),
    # Input('apply-filters-button', 'n_clicks'),
    [Input('filter-periode-construction', 'value'),
     Input('filter-DPE', 'value'),
     Input('filter-type-batiment', 'value')]
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
