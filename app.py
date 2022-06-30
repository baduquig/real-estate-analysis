from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from tenacity import retry

app = Dash(__name__)

df = pd.read_csv('./data/zvhi_3bed.csv')

state_dropdown_values = df['State'].unique()


"""
def set_plot(data_frame, lowest_level, state, city):
    print('lowest_level: ' + lowest_level)
    if lowest_level == 'State':
        data_frame[data_frame['State'].isin(state)]
        data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName'], axis=1)
        data_frame = data_frame.groupby(['City']).mean()
        data_frame = data_frame.transpose()
    elif lowest_level == 'City':
        data_frame[data_frame['State'].isin(state)]
        data_frame[data_frame['City'].isin(city)]
        data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], axis=1)
        data_frame = data_frame.groupby(['RegionName']).mean()
        data_frame = data_frame.transpose()
    else:
        data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], axis=1)
        data_frame = data_frame.mean()
        data_frame = data_frame.transpose()
        
    return data_frame
"""


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
    Input('state', 'value')
)
def set_city_options(selected_states):
    cities = df[df['State'].isin(list(selected_states))]
    return cities['City'].unique()

@app.callback(
    Output('zipcode', 'options'),
    Input('state', 'value'),
    Input('city', 'value')
)
def set_zip_options(selected_states, selected_cities):
    zip_codes = df[df['State'].isin(list(selected_states))]
    zip_codes = zip_codes[zip_codes['City'].isin(list(selected_cities))]
    return zip_codes['RegionName'].unique()

@app.callback(
    Output('hpi-line-graph', 'figure'),
    Input('state', 'value'),
    Input('city', 'value')
)
def set_city_plot(selected_states, selected_cities):
    data_frame = df
    if len(selected_cities) > 0:
        data_frame = data_frame[data_frame['State'].isin(selected_states)]
        data_frame = data_frame[data_frame['City'].isin(selected_cities)]
    else: 
        data_frame = data_frame[data_frame['State'].isin(selected_states)]

    data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], axis=1)
    data_frame = data_frame.mean()
    data_frame = data_frame.transpose()
    return px.line(data_frame)

"""
@app.callback(
    Output('hpi-line-graph', 'figure'),
    Input('state', 'value'),
    Input('city', 'value')
)
def set_plot(selected_states, selected_cities):
    data_frame = df
    data_frame[data_frame['State'].isin(selected_states)]
    data_frame[data_frame['City'].isin(selected_cities)]
    data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName'], axis=1)
    data_frame = data_frame.groupby(['RegionName']).mean()
    data_frame = data_frame.transpose()
    return px.line(data_frame)
"""
#~~~ Callbacks ~~~#
    

if __name__ == '__main__':
    app.run_server(debug=True)
