from dash import html, dcc, Input, Output
import pandas as pd
import branca
import folium
from folium.plugins import MarkerCluster
from config import app, load_data


data_energy = load_data()
data_energy = data_energy.dropna(subset=['nom_commune'])
etiquet_dpe = data_energy['Etiquette_DPE'].unique().tolist()
communes = ['All'] + data_energy['nom_commune'].unique().tolist()

title_map = html.Div(
    children=[
        html.Img(src="./assets/earth.ico", className="header-emoji"),
        html.H1(
            children="Cartographie des Consommations Énergétiques", className="header-title"
        ),
        html.P(
            children=(
                "Analysez la consommation énergétique"
                " en fonction de la localisation."
            ),
            className="header-description",
        ),
    ],
    className="header", style={"backgroundColor": "#02733E"},
)

form_filter_map = html.Div(
    children=[
        html.Label("Étiquette DPE", style={'margin-bottom': '10px'}),
        dcc.Dropdown(
            id='dpe-filter',
            options=[{'label': label, 'value': label} for label in etiquet_dpe],
            placeholder="Sélectionnez une étiquette DPE"
        ),
        html.Label("Commune", style={'margin-bottom': '10px', 'margin-top': '10px'}),
        dcc.Dropdown(
            id='commune-filter',
            options=[{'label': commune, 'value': commune} for commune in communes],
            placeholder="Sélectionnez une commune",
            multi=True
        ),
        html.Label("Coût Chauffage (€)", style={'margin-bottom': '10px', 'margin-top': '10px'}),
        dcc.RangeSlider(
            id='cost-slider',
            min=data_energy['Coût_chauffage'].min(),
            max=data_energy['Coût_chauffage'].max(),
            step=1,
            value=[data_energy['Coût_chauffage'].min(), data_energy['Coût_chauffage'].max()],
            marks={int(val): str(int(val)) for val in data_energy['Coût_chauffage'].quantile([0, 0.25, 0.5, 0.75, 1]).tolist()}
        ),
        html.Div(
            id='cost-range-display', style={
                'marginTop': '10px',
                'marginBottom': '10px',
                'fontWeight': 'bold',
                'fontSize': '13px',
                'color': '#0d6efd'
            }
        ),
        html.Button(
            'Submit', id='submit-button', n_clicks=0, style={
                'backgroundColor': '#0d6efd',
                'color': 'white',
                'padding': '15px 32px',
                'textAlign': 'center',
                'textDecoration': 'none',
                'display': 'inline-block',
                'fontSize': '16px',
                'margin': '4px 2px',
                'cursor': 'pointer',
                'border': 'none',
                'borderRadius': '4px'
            }
        )
    ], className='menuMap'
)


@app.callback(
    Output('cost-range-display', 'children'),
    Input('cost-slider', 'value')
)
def update_cost_range_display(selected_cost):
    """Update the display of the selected cost range."""
    return f"Selected range: {selected_cost[0]}€ to {selected_cost[1]}€"


def map_page(collapsed):
    """Render the map page layout."""
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    full_body = html.Div(
        children=[
            html.Div(
                children=[
                    title_map,
                    html.Div(
                        children=[
                            html.Div(
                                children=[form_filter_map],
                                style={
                                    'width': '30%',
                                    'display': 'inline-block',
                                    'verticalAlign': 'top',
                                }
                            ),
                            html.Div(
                                id='map-container',
                            )
                        ], style={'display': 'flex', 'margin-top': '20px'}
                    )
                ], className=pagecontent_class, id="PageAnalytics"
            ),
        ]
    )

    return full_body


@app.callback(
    Output('map-container', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('dpe-filter', 'value'),
    Input('commune-filter', 'value'),
    Input('cost-slider', 'value')
)
def update_map(n_clicks, selected_dpe, selected_commune, selected_cost):
    """Update the map based on the selected filters."""
    if n_clicks > 0:
        filtered_data = filter_data(selected_dpe, selected_commune, selected_cost)
        if filtered_data.empty:
            return html.Div(
                "No data found in the database for the selected filter.", style={
                    'color': '#0d6efd',
                    'fontWeight': 'bold',
                    'fontSize': '16px',
                    'textAlign': 'center',
                    'marginTop': '20px'
                }
            )
        return render_filtered_map(filtered_data)
    return html.Div(
        "Select some option", style={
            'color': '#0d6efd',
            'fontWeight': 'bold',
            'fontSize': '16px',
            'textAlign': 'center',
            'marginTop': '20px'
        }
    )


def filter_data(selected_dpe, selected_commune, selected_cost):
    """Filter the data based on the selected filters."""
    filtered_data = data_energy
    if selected_dpe:
        filtered_data = filtered_data[filtered_data['Etiquette_DPE'] == selected_dpe]
    if selected_commune and 'All' not in selected_commune:
        filtered_data = filtered_data[filtered_data['nom_commune'].isin(selected_commune)]
    if selected_cost:
        filtered_data = filtered_data[
            (filtered_data['Coût_chauffage'] >= selected_cost[0]) & (filtered_data['Coût_chauffage'] <= selected_cost[1])
        ]
    return filtered_data


def render_filtered_map(data):
    """Render the filtered data on a folium map."""
    etiquet_dpe_color_dict = {
        'A': '#008000',
        'B': '#B5E61D',
        'C': '#FFD700',
        'D': '#FFA500',
        'E': '#FF0000'
    }
    m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=10, tiles="cartodb positron")
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in data.iterrows():
        html_popup = (
            f"<div style='font-family: system-ui;'>"
            f"<b>Coût Chauffage:</b> {row['Coût_chauffage']} €<br>"
            f"<b>Surface Habitable:</b> {row['Surface_habitable_logement']} m² <br>"
        )
        color = etiquet_dpe_color_dict.get(row['Etiquette_DPE'], '#000000')
        html_popup += f"<b>Étiquette DPE:</b> <span style='color:{color}'>{row['Etiquette_DPE']}</span><br>"

        iframe = branca.element.IFrame(html=html_popup, width=300, height=100)
        popup = folium.Popup(iframe, max_width=500)
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=popup,
            tooltip=row['Adresse_(BAN)']
        ).add_to(marker_cluster)

    map_html = m._repr_html_()
    map_iframe = html.Iframe(srcDoc=map_html, width='100%', height='600')
    return html.Div(children=[map_iframe], style={'width': '100%', 'display': 'inline-block'})
