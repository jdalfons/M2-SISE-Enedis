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

fields = ['Date_réception_DPE',
          'Etiquette_DPE',
          'Coût_chauffage',
          'Surface_habitable_logement',
          'Adresse_(BAN)',
          'Code_postal_(BAN)',
          'Identifiant__BAN',]

# Get addresses info from 69 department
addresses_df = pd.read_csv('./data/adresses-69.csv', sep=';')

# Read the CSV file into a DataFrame with specified data types
data_energy = pd.read_csv('./data/data_output.csv', dtype=dtype, low_memory=False, names=fields, header=0)

# Perform the merge operation
data_energy = data_energy.merge(addresses_df, left_on='Identifiant__BAN', right_on='id', how='left')

# Convert date column to datetime
data_energy['Date_réception_DPE'] = pd.to_datetime(data_energy['Date_réception_DPE'], format="%Y-%m-%d")

# Remove outliers based on the IQR method for 'Coût_chauffage' and 'Surface_habitable_logement'
Q1 = data_energy[['Coût_chauffage', 'Surface_habitable_logement']].quantile(0.25)
Q3 = data_energy[['Coût_chauffage', 'Surface_habitable_logement']].quantile(0.75)
IQR = Q3 - Q1

data_energy = data_energy[~((data_energy[['Coût_chauffage', 'Surface_habitable_logement']] < (Q1 - 1.5 * IQR)) | (data_energy[['Coût_chauffage', 'Surface_habitable_logement']] > (Q3 + 1.5 * IQR))).any(axis=1)]

# Drop rows with missing latitude or longitude
data_energy = data_energy.dropna(subset=['lat', 'lon'])

# Get unique DPE labels
etiquet_dpe = data_energy['Etiquette_DPE'].cat.categories

# Get unique commune names and add "All" option
communes = ['All'] + addresses_df['nom_commune'].unique().tolist()

global new_click 
global old_click 
new_click = 0
old_click = 0

title_map = html.H2("Cartographie des Consommations Énergétiques")
subtitle_map = html.P("Analysez la consommation énergétique en fonction de la localisation.")
form_filter_map = html.Div(children=[
    html.Label("Étiquette DPE"),
    dcc.Dropdown(
        id='dpe-filter',
        options=[{'label': label, 'value': label} for label in etiquet_dpe],
        placeholder="Sélectionnez une étiquette DPE"
    ),
    html.Label("Commune"),
    dcc.Dropdown(
        id='commune-filter',
        options=[{'label': commune, 'value': commune} for commune in communes],
        placeholder="Sélectionnez une commune",
        multi=True
    ),
    html.Label("Coût Chauffage (€)"),
    dcc.RangeSlider(
        id='cost-slider',
        min=data_energy['Coût_chauffage'].min(),
        max=data_energy['Coût_chauffage'].max(),
        step=1,
        value=[data_energy['Coût_chauffage'].min(), data_energy['Coût_chauffage'].max()],
        marks={int(val): str(int(val)) for val in data_energy['Coût_chauffage'].quantile([0, 0.25, 0.5, 0.75, 1]).tolist()}
    ),
    html.Div(id='cost-range-display', style={
        'marginTop': '10px',
        'marginBottom': '10px',
        'fontWeight': 'bold',
        'fontSize': '13px',
        # 'textAlign': 'center',
        'color': '#0d6efd'}),
    html.Button('Submit', id='submit-button', n_clicks=0, style={
        'backgroundColor': '#0d6efd',  # Blue background
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
    })
])

@app.callback(
    Output('cost-range-display', 'children'),
    Input('cost-slider', 'value')
)
def update_cost_range_display(selected_cost):
    return f"Selected range: {selected_cost[0]}€ to {selected_cost[1]}€"

def map_page(collapsed):
    pagecontent_class = "page-content collapsed" if collapsed else "page-content"
    full_body = html.Div(children=[
        title_map,
        subtitle_map,
        html.Div(children=[
            html.Div(children=[form_filter_map], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div(id='map-container', style={
                'width': '70%', 
                'display': 'inline-block',
                'verticalAlign': 'top',
                'padding': '10px',
                'border': '1px solid #d3d3d3',
                'backgroundColor': '#f8f9fa',
                'height': '450px',
                'margin': '10px',
                'borderRadius': '15px',
                })
        ], style={'display': 'flex'})
    ],  
                         className=pagecontent_class,
                         id="pageMap"
    )
    return full_body

@app.callback(
    Output('map-container', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('dpe-filter', 'value'),
    Input('commune-filter', 'value'),
    Input('cost-slider', 'value'))
def update_map(n_clicks, selected_dpe, selected_commune, selected_cost):
    global new_click, old_click
    if n_clicks > old_click:
        old_click = n_clicks
        filtered_data = data_energy
        if selected_dpe:
            filtered_data = filtered_data[filtered_data['Etiquette_DPE'] == selected_dpe]
        if selected_commune and 'All' not in selected_commune:
            filtered_data = filtered_data[filtered_data['nom_commune'].isin(selected_commune)]
        if selected_cost:
            filtered_data = filtered_data[(filtered_data['Coût_chauffage'] >= selected_cost[0]) & (filtered_data['Coût_chauffage'] <= selected_cost[1])]
        if filtered_data.empty:
            return html.Div("No data found in the database for the selected filter.", style={
        'color': '#0d6efd',  # Red text
        'fontWeight': 'bold',
        'fontSize': '16px',
        'textAlign': 'center',
        'marginTop': '20px'
        }), ""
        return render_filtered_map(filtered_data)
    return html.Div("Select some option", style={
        'color': '#0d6efd',  # Red text
        'fontWeight': 'bold',
        'fontSize': '16px',
        'textAlign': 'center',
        'marginTop': '20px'
    }), ""

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
