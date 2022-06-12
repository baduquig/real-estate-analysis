from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('./data/zvhi_3bed.csv')

state_dropdown_values = df['State'].unique()

df = df[df['State']=='AZ']
df = df[df['City'].isin(['Chandler', 'Tempe', 'Mesa', 'Gilbert'])]
df = df.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName'], axis=1)
df = df.groupby(['City']).mean()
df = df.transpose()


fig = px.line(df)


app.layout = html.Div([
    html.H1('3 bedroom housing prices in Phoenix, AZ'),

    html.Div('Time series data analysis of 3 bedroom homes in the east valley'),

    html.Div([
        dcc.Dropdown(
            state_dropdown_values,
            'Select a state',
            id='state',
            multi=True
        )
    ]),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
