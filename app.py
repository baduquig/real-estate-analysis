from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('./data/zvhi_3bed.csv')

lowest_level = 'State'
state_dropdown_values = df['State'].unique()

state = []
city = []
zipcode = []

def set_plot(data_frame, lowest_level, state, city):
    if lowest_level == 'State':
        data_frame = data_frame[data_frame['State'].isin(state)]
    else:
        data_frame = data_frame[data_frame['State'].isin(state)]
        data_frame = data_frame[data_frame['City'].isin(city)]        
    data_frame = data_frame.groupby([lowest_level]).mean()
    data_frame = data_frame.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName'], axis=1)
    data_frame = data_frame.transpose()
    return data_frame

fig = px.line(set_plot(df, lowest_level, state, city))

app.layout = html.Div([
    html.H1('3 bedroom housing prices in Phoenix, AZ'),

    html.Div('Time series data analysis of 3 bedroom homes in the east valley'),

    html.Div([
        html.Label('State'),
        dcc.Dropdown(
            state_dropdown_values,
            'AZ',
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
        id='example-graph',
        figure=fig
    )
])
#~~~ End app.layout ~~~#

#~~~ Callbacks ~~~#
@app.callback(
    Output('city', 'options'),
    Input('state', 'value')
)
def set_cities(selected_states):
    lowest_level = 'State'
    return df[df['City'].isin([selected_states])].unique()

@app.callback(
    Output('zipcode', 'options'),
    Input('city', 'value')
)
def zip_codes(selected_cities):
    lowest_level = 'City'
    return df[df['RegionName'].isin([selected_cities])].unique()
#~~~ Callbacks ~~~#
    

if __name__ == '__main__':
    app.run_server(debug=True)
