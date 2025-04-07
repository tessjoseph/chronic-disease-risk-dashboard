import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

# Read the CSV
df = pd.read_csv('U.S._Chronic_Disease_Indicators_20241014.csv')

# Select necessary columns
columns = ["YearStart", "YearEnd", "LocationAbbr", "LocationDesc", "DataSource", "Topic", "Question",
           "DataValue", "DataValueAlt", "DataValueFootnoteSymbol", "DataValueFootnote", "LowConfidenceLimit",
           "HighConfidenceLimit", "StratificationCategory1", "Stratification1", "StratificationID1", "Geolocation"]
df = df[columns]


# Initialize the app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Dropdown(
        options=[{'label': loc, 'value': loc} for loc in df['LocationAbbr'].unique()],
        id='location-dropdown',
        placeholder='Where do you live?'
    ),
    dcc.Dropdown(
        options=[{'label': topic, 'value': topic} for topic in df['Topic'].unique()],
        id='topic-dropdown',
        placeholder='What disease do you have?'
    ),
    dcc.Dropdown(
        options=[{'label': question, 'value': question} for question in df['Question'].unique()],
        id='question-dropdown',
        placeholder='What question do you want to answer about your disease?'
    ),

    html.Div(id='choropleth-container')  # Div to hold the choropleth graph
])

# Define the callback to generate the graph based on dropdowns
@app.callback(
    Output('choropleth-container', 'children'),
    [Input('location-dropdown', 'value'),
     Input('topic-dropdown', 'value'),
     Input('question-dropdown', 'value')]
)
def update_graph(location, topic, question):
    if not location or not topic or not question:
        return "Please select a location, topic, and question."

    # Filter the dataframe based on user selection
    filtered_df = df[(df['LocationAbbr'] == location) &
                     (df['Topic'] == topic) &
                     (df['Question'] == question)]

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
