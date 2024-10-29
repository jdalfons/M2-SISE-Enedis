# pages/map.py
from dash import html, dcc, Input, Output
import pandas as pd
import branca
import folium
from folium.plugins import MarkerCluster
from config import app

app.config.suppress_callback_exceptions = True

# Define data types for the CSV columns
dtype = {
    'Date_réception_DPE': 'str',
    'lat': 'float64',
    'lon': 'float64',
    'Etiquette_DPE': 'category',
    'Coût_chauffage': 'float64',
    'Surface_habitable_logement': 'float64',
    'Adresse_(BAN)': 'str'
}

# Read the CSV file into a DataFrame with specified data types
data_energy = pd.read_csv('./data/merged_data_test.csv', dtype=dtype, low_memory=False)

# Convert date column to datetime
data_energy['Date_réception_DPE'] = pd.to_datetime(data_energy['Date_réception_DPE'], format="%Y-%m-%d")

# Drop rows with missing latitude or longitude
data_energy = data_energy.dropna(subset=['lat', 'lon'])

# Get unique DPE labels
etiquet_dpe = data_energy['Etiquette_DPE'].cat.categories

# Limit the data to 150 rows
data_energy = data_energy.head(1000)

global new_click 
global old_click 
new_click = 0
old_click = 0

title_map = html.H2("Cartographie des Consommations Énergétiques")
subtitle_map = html.P("Analysez la consommation énergétique en fonction de la localisation.")
form_filter_map = html.Div(children=[
    dcc.Dropdown(
        id='dpe-filter',
        options=[{'label': label, 'value': label} for label in etiquet_dpe],
        placeholder="Sélectionnez une étiquette DPE",
        multi=True
    ),
    html.Button('Submit', id='submit-button', n_clicks=0)
])

def map_page(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    full_body = html.Div(children=[
        title_map,
        subtitle_map,
        html.Div(children=[
            html.Div(children=[form_filter_map], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div(id='map-container', style={'width': '70%', 'display': 'inline-block'})
        ], style={'display': 'flex'})
    ],  
                         className=pagecontent_class,
                         id="pageMap"
    )
    return full_body

@app.callback(
    Output('map-container', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('dpe-filter', 'value'))
def update_map(n_clicks, selected_dpe):
    global new_click, old_click
    new_click += 1
    if new_click > old_click and selected_dpe:
        old_click = new_click
        filtered_data = data_energy[data_energy['Etiquette_DPE'].isin(selected_dpe)]
        if filtered_data.empty:
            return html.Div("No data found in the database for the selected filter.")
        return render_filtered_map(filtered_data)
    return html.Div("Select some option")

def render_filtered_map(data, collapsed=True):
    etiquet_dpe_color_dict = {
        'A': '#008000',
        'B': '#B5E61D',
        'C': '#FFD700',
        'D': '#FFA500',
        'E': '#FF0000'
    }
    # Create a base map centered at the mean latitude and longitude with a different tileset
    m = folium.Map(location=[data['lat'].mean(), data['lon'].mean()], zoom_start=10, tiles="cartodb positron")

    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Add points to the map
    for _, row in data.iterrows():
        html_popup = (
            f"<div style='font-family: system-ui;'>"
            f"<b>Coût Chauffage:</b> {row['Coût_chauffage']} €<br>"
            f"<b>Surface Habitable:</b> {row['Surface_habitable_logement']} m² <br>"
        )
        color = etiquet_dpe_color_dict.get(row['Etiquette_DPE'], '#000000')  # Default to black if not found
        html_popup += f"<b>Étiquette DPE:</b> <span style='color:{color}'>{row['Etiquette_DPE']}</span><br>"
        
        iframe = branca.element.IFrame(html=html_popup, width=300, height=100)
        popup = folium.Popup(iframe, max_width=500)
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=popup,
            tooltip=row['Adresse_(BAN)']
        ).add_to(marker_cluster)

    # Save the map to an HTML string
    map_html = m._repr_html_()

    # Create an Iframe to embed the folium map
    map_iframe = html.Iframe(srcDoc=map_html, width='100%', height='600')

    return html.Div(id='map-container', children=[map_iframe], style={'width': '100%', 'display': 'inline-block'})
