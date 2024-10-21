"""
This module sets up a Dash application for managing and displaying configuration thresholds.

The application features:
1. A table for viewing and editing thresholds.
2. A button to save the updated threshold values to a data source.

The Dash app is initialized with a specific URL prefix and is designed to be accessible at the '/configs/' endpoint.
"""

from flask import Flask
import dash
from dash import dash_table, html
from dash.dependencies import Input, Output, State
import pandas as pd
from weather_service.utils import thresholds

def load_data():
    """
    Fetch the latest threshold data and convert it to a DataFrame.

    Returns:
    pd.DataFrame: The DataFrame containing threshold data.
    """
    data = thresholds.get_thresholds()
    return pd.DataFrame(data)

# Initialize Dash app with a specific URL prefix
app = dash.Dash(__name__, requests_pathname_prefix='/configs/')

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Thresholds"),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in load_data().columns],
        data=load_data().to_dict('records'),
        editable=True,
    ),
    html.Button("Save Value", id="btn_csv"),
])

# Define the callback to update the thresholds data
@app.callback(
    Output('table', 'data'),
    Input("btn_csv", "n_clicks"),
    State('table', 'data'),
    prevent_initial_call=True,
)
def save_values(n_clicks, rows):
    """
    Save the updated threshold values to the data source.

    Parameters:
    n_clicks (int): The number of times the "Save Value" button has been clicked.
    rows (list): The current data in the table.

    Returns:
    list: The updated data in the table.
    """
    new_data = pd.DataFrame(rows).to_dict('list')
    for key, rdata in new_data.items():
        new_data[key] = [int(i) for i in rdata]

    thresholds.update_thresholds(**new_data)
    
    return rows

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
