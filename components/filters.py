# filters.py
from dash import dcc, html
import dash_bootstrap_components as dbc

# Composant de radio button
def render_radio_button(id, options, value=None, label=None):
    return html.Div(
        [
            html.Label(label, className="filter-label"),
            dcc.RadioItems(
                id=id,
                options=[{"label": opt, "value": opt} for opt in options],
                value=value,
                className="filter-radio"
            )
        ],
        className="filter-container"
    )

# Composant de slider
def render_slider(id, min_val, max_val, step, value, label=None):
    return html.Div(
        [
            html.Label(label, className="filter-label"),
            dcc.Slider(
                id=id,
                min=min_val,
                max=max_val,
                step=step,
                value=value,
                marks={str(i): str(i) for i in range(min_val, max_val+1, step)},
                className="filter-slider"
            )
        ],
        className="filter-container"
    )

# Composant de checkbox
def render_checkbox(id, options, values=None, label=None):
    return html.Div(
        [
            html.Label(label, className="filter-label"),
            dcc.Checklist(
                id=id,
                options=[{"label": opt, "value": opt} for opt in options],
                value=values,
                className="filter-checkbox"
            )
        ],
        className="filter-container"
    )

# Composant de dropdown (select)
def render_dropdown(id, options, value=None, label=None, multi=False):
    return html.Div(
        [
            html.Label(label, className="filter-label"),
            dcc.Dropdown(
                id=id,
                options=[{"label": opt, "value": opt} for opt in options],
                value=value,
                multi=multi,
                className="filter-dropdown"
            )
        ],
        className="filter-container"
    )
