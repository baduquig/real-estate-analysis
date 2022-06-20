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


fig =px.line(set_plot(df, lowest_level, state, city))

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
    Output('hpi-line-graph', 'figure'),
    Input('state', 'value'),
    Input('city', 'value')
)
def set_plot(
    
)

"""@app.callback(
    Output('city', 'value'),
    Input('city', 'options')
)
def set_city_values(available_cities):
    return available_cities[['City']]

@app.callback(
    Output('zipcode', 'options'),
    Input('city', 'value')
)
def zip_codes(selected_cities):
    return df[df['RegionName'].isin([selected_cities]).unique()]"""
#~~~ Callbacks ~~~#
    

if __name__ == '__main__':
    app.run_server(debug=True)
