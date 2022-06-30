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
    Input('city', 'value'),
    Input('zipcode', 'value')
)
def set_city_plot(selected_states, selected_cities, selected_zipcodes):
    data_frame = df

    if ((selected_states is None) and (selected_cities is None) and (selected_zipcodes is None)):
        pass
    elif((selected_cities is None) and (selected_zipcodes is None)):
        data_frame = data_frame[data_frame['State'].isin(selected_states)]
        data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'State', 'City', 'Metro', 'CountyName'], axis=1)
    elif(selected_zipcodes is None):
        data_frame = data_frame[data_frame['State'].isin(selected_states)]
        data_frame = data_frame[data_frame['City'].isin(selected_cities)]
        data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName'], axis=1)
    else:
        data_frame = data_frame[data_frame['State'].isin(selected_states)]
        data_frame = data_frame[data_frame['City'].isin(selected_cities)]
        data_frame = data_frame[data_frame['RegionName'].isin(selected_zipcodes)]
        data_frame = data_frame.groupby('RegionName')
        

    data_frame = data_frame.mean()
    data_frame = data_frame.transpose()
    return px.line(data_frame)

    """
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

#~~~ Callbacks ~~~#
    

if __name__ == '__main__':
    app.run_server(debug=True)
