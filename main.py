import dash
from dash import dcc, html
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Try to read the data
try:
    df = pd.read_csv('data/EnedisData.csv')
    data_found = True
except FileNotFoundError:
    data_found = False

# Define the layout
app.layout = html.Div([
    html.H1("Enedis Data Dashboard"),
    html.Div(id='data-status'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # in milliseconds (e.g., 60 seconds)
        n_intervals=0
    )
])

# Update the data status
@app.callback(
    dash.dependencies.Output('data-status', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_data_status(n):
    if data_found:
        return html.Div([
            html.H2("Data Loaded Successfully"),
            # Add more components to display data here
        ])
    else:
        return html.H2("No data found")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)