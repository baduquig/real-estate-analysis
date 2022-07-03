from re import A
from select import select
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from tenacity import retry

app = Dash(__name__)

df = pd.read_csv('./data/zvhi_3bed.csv')

state_dropdown_values = df['State'].unique()


app.layout = html.Div([
    html.H1('3 bedroom housing prices in the United States'),

    html.Div('Time series data analysis of 3 bedroom homes'),

    html.Div([
        html.Label('State'),
        dcc.Dropdown(
            state_dropdown_values,
            id='state',
            multi=True
        ),

        html.Label('City'),
        dcc.Dropdown(
            id='city',
            multi=True
        ),

        html.Label('Zipcode(s)'),
        dcc.Dropdown(
            id='zipcode',
            multi=True
        )
    ]),

    dcc.Graph(
        id='hpi-line-graph'
    )
])
#~~~ End app.layout ~~~#


#~~~ Callbacks ~~~#
@app.callback(
    Output('city', 'options'),
    Input('state', 'value'),
    prevent_initial_call=True
)
def set_city_options(selected_states):
    cities = df[df['State'].isin(list(selected_states))]
    cities = cities['City'].unique()
    return cities


@app.callback(
    Output('zipcode', 'options'),
    Input('state', 'value'),
    Input('city', 'value'),
    prevent_initial_call=True
)
def set_zip_options(selected_states, selected_cities):
    if (selected_cities is None or selected_cities == []):
        zip_codes = []
    else:
        zip_codes = df[df['State'].isin(list(selected_states))]
        zip_codes = zip_codes[zip_codes['City'].isin(list(selected_cities))]
        zip_codes = zip_codes['RegionName'].unique()
    return zip_codes


@app.callback(
    Output('hpi-line-graph', 'figure'),
    Input('state', 'value'),
    Input('city', 'value'),
    Input('zipcode', 'value')
)
def set_city_plot(selected_states, selected_cities, selected_zipcodes):
    data_frame = df
    print('selected_states: ' + str(selected_states))
    print('selected_cities: ' + str(selected_cities))
    print('selected_zipcodes: ' + str(selected_zipcodes))
    if ((selected_states is None or selected_states == []) 
    and (selected_cities is None or selected_cities == []) 
    and (selected_zipcodes is None or selected_zipcodes == [])):
        data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], axis=1)
    elif((selected_cities is None or selected_cities == []) and (selected_zipcodes is None or selected_zipcodes == [])):
        data_frame = data_frame[data_frame['State'].isin(selected_states)]
        data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'City', 'Metro', 'CountyName'], axis=1)
        data_frame = data_frame.groupby('State')
    elif(selected_zipcodes is None or selected_zipcodes == []):
        data_frame = data_frame[data_frame['State'].isin(selected_states)]
        data_frame = data_frame[data_frame['City'].isin(selected_cities)]
        data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName'], axis=1)
        data_frame = data_frame.groupby('City')
    else:
        data_frame = data_frame[data_frame['State'].isin(selected_states)]
        data_frame = data_frame[data_frame['City'].isin(selected_cities)]
        data_frame = data_frame[data_frame['RegionName'].isin(selected_zipcodes)]
        data_frame = data_frame.groupby('RegionName')        

    data_frame = data_frame.mean()
    data_frame = data_frame.transpose()
    return px.line(data_frame)

#~~~ Callbacks ~~~#
    

if __name__ == '__main__':
    app.run_server(debug=True)
