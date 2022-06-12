from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('./data/zvhi_3bed.csv')
df = df[df['State']=='AZ']
df = df[df['City'].isin(['Chandler', 'Tempe', 'Mesa', 'Gilbert'])]
df = df.drop(['RegionID', 'SizeRank', 'RegionName', 'RegionName', 'RegionType', 'StateName', 'State', 'Metro', 'CountyName'], axis=1)
df = df.groupby(['City']).mean()
df = df.transpose()


fig = px.line(df)


app.layout = html.Div(children=[
    html.H1(children='3 bedroom housing prices in Phoenix, AZ'),

    html.Div(children='Time series data analysis of 3 bedroom homes in the east valley'),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
