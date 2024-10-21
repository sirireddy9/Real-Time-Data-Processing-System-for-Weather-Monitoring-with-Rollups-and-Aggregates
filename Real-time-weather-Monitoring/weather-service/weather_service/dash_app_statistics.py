"""
This module sets up a Dash application for visualizing weather data. 

The application provides two main features:
1. Real-time data visualization: Displays a line plot for real-time weather data, which updates based on user input from a dropdown menu.
2. Historical data visualization: Shows line plots for average, maximum, and minimum temperatures over time.

The Dash app is initialized with a specific URL prefix and is designed to display weather statistics at the '/statistics/' endpoint.
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from weather_service.db_utils import get_historical_data, get_realtime_data

# Initialize the Dash app with a specific URL prefix
app = dash.Dash(
    __name__,
    requests_pathname_prefix='/statistics/'
)

def plot_data_r(data, col):
    """
    Create a line plot for real-time data.

    Parameters:
    data (pd.DataFrame): The data to be plotted
    col (str): The column to be plotted on the y-axis

    Returns:
    dcc.Graph: The generated Plotly graph
    """
    fig = px.line(data, x='dt', y=col, color='city', line_group='city',
                  labels={'temp': 'Temperature', 'dt': 'Date'})
    return dcc.Graph(figure=fig)

def plot_data_h(data, col):
    """
    Create a line plot for historical data.

    Parameters:
    data (pd.DataFrame): The data to be plotted
    col (str): The column to be plotted on the y-axis

    Returns:
    dcc.Graph: The generated Plotly graph
    """
    fig = px.line(data, x='date', y=col, color='city', barmode='group',
                  labels={'temp': 'Temperature', 'date': 'Date'})
    return dcc.Graph(figure=fig)

@app.callback(
    Output("graph_realtime", "children"), 
    Input("dropdown_r", "value")
)
def update_bar_chart(data_type):
    """
    Update the real-time data chart based on the selected data type.

    Parameters:
    data_type (str): The selected data type from the dropdown

    Returns:
    dcc.Graph: The updated Plotly graph
    """
    realtime_data = pd.DataFrame(eval(get_realtime_data()))
    return plot_data_r(realtime_data, data_type)

def plot_historical_data():
    """
    Generate the layout for historical data plots.

    Returns:
    list: A list of HTML Div components containing the historical data plots
    """
    historical_data = pd.DataFrame(eval(get_historical_data()))
    if historical_data.empty:
        return html.H2("No historical data available.")
    
    return [
        html.Div([
            html.H2("Average Temp vs Time"),
            plot_data_h(historical_data, 'avg_temp')
        ]),
        html.Div([
            html.H2("Max Temp vs Time"),
            plot_data_h(historical_data, 'max_temp')
        ]),
        html.Div([
            html.H2("Min Temp vs Time"),
            plot_data_h(historical_data, 'min_temp')
        ])
    ]

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Weather Data Historical and Realtime"),
    html.Div(id='realtime-chart', title="Realtime Weather Data", children=[
        dcc.Dropdown(
            id="dropdown_r",
            options=[
                {'label': 'Temperature', 'value': 'temp'},
                {'label': 'Humidity', 'value': 'humidity'},
                {'label': 'Pressure', 'value': 'pressure'},
                {'label': 'Clouds', 'value': 'clouds'}
            ],
            value="temp",
            clearable=False,
        ),
        html.Div(id="graph_realtime")
    ]),
    html.Div(id='historical-chart', title="Historical Weather Data", children=plot_historical_data()),
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
