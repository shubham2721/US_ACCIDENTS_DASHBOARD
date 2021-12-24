import pandas as pd
import numpy as np
import seaborn as sns
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.express.colors as colors
import datetime

df = pd.read_csv('US_ACCIDENTS_2020.csv')

# we will create a counter column for calculating the accident each time based on unique states
df['accident_count'] = 1
# or df['State'].value_counts()

state_full_name = pd.read_csv('csvData.csv')
state_full_name.rename(columns = {'Code': 'State', 'State' : 'State Full Name'}, inplace = True)

# Left joining the data set and storign it to accidents
accidents = pd.merge(df, state_full_name, on = 'State', how = 'left') # how = ['left', 'inner', 'right', 'outer']

# Grouping the above dataframe based on code and state full name 
accident_count_state_wise = accidents.groupby(['State', 'State Full Name']).sum()
# accident_count_state_wise.index.get_level_values(0) for viewing the firsst index

accidents['Temperature(F)'] = pd.to_numeric(accidents['Temperature(F)'], errors ='coerce')
accidents['Humidity(%)'] = pd.to_numeric(accidents['Humidity(%)'], errors ='coerce')
accidents['Pressure(in)'] = pd.to_numeric(accidents['Pressure(in)'], errors ='coerce')
accidents['Visibility(mi)'] = pd.to_numeric(accidents['Visibility(mi)'], errors ='coerce')
accidents['Wind_Speed(mph)'] = pd.to_numeric(accidents['Wind_Speed(mph)'], errors ='coerce')
accidents['Start_Time'] = pd.to_datetime(accidents['Start_Time'], errors = 'coerce')

accidents['year'] = accidents['Start_Time'].dt.year
accidents2020 = accidents[accidents['year'] == 2020.0].reset_index()
accident_count_state_wise = accidents2020.groupby(['State', 'State Full Name']).sum()

accidents2020['day'] = accidents2020['Start_Time'].dt.strftime('%a')
accidents2020['month'] = accidents2020['Start_Time'].dt.strftime('%B')

FA = "https://use.fontawesome.com/releases/v5.12.1/css/all.css"

# DASHBOARD

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FA])
server = app.server

app.layout = html.Div(style={'background-color': '#4C4948'}, 
                      children =[dbc.Row(dbc.Col(
                          html.H1("US ACCIDENTS 2020 DASHBOARD",style = {'textAlign' : 'center', 'fontWeight' : 'bold', 'color': 'white'}))),
    html.Br(),
    dbc.Row([dbc.Col(
        dbc.Card(dbc.CardBody(
            [
                html.P("Average Temperature", style = {'textAlign' : 'center', 'color': 'white', 'font-size': 13}),
                dbc.Row([dbc.Col(html.I(className="fas fa-temperature-low fa-lg", style={'color': 'red'}),width = {'size': 2, 'offset':1}),
                    dbc.Col(html.H4(f"{round(accidents2020['Temperature(F)'].mean(), 2)} F", style = {'color' : 'Red',
                                                                                    'textAlign' : 'left',
                                                                                    'fontWeight' : 'bold'}))
                         ])
            ],
        ),style = {'backgroundColor' : '#141414', "margin-left": "15px"})),
        dbc.Col(dbc.Card(dbc.CardBody(
            [
                html.P("Average Humidity", style = {'textAlign' : 'center', 'color': 'white', 'font-size': 13}),
                dbc.Row([dbc.Col(html.I(className="fas fa-cloud fa-lg", style={'color': 'Blue'}),width = {'size': 1, 'offset': 1}),
                    dbc.Col(html.H4(f"{round(accidents2020['Humidity(%)'].mean(),2)} %", style = {'color' : 'Blue',
                                                                                               'textAlign' : 'center',
                                                                                                'fontWeight' : 'bold'}),width = {'offset': 0})
                        ])
            ],
        ),style = {'backgroundColor' : '#141414'})),
        dbc.Col(dbc.Card(dbc.CardBody(
            [
                html.P("Average Pressure", style = {'textAlign' : 'center', 'color': 'white', 'font-size': 13}),
                dbc.Row([dbc.Col(html.I(className="fas fa-atom fa-lg", style={'color': 'Green'}),width = {'size': 1, 'offset': 1}),
                    dbc.Col(html.H4(f"{round(accidents2020['Pressure(in)'].mean(),2)} inHG", style = {'color' : 'Green',
                                                                                               'textAlign' : 'center',
                                                                                                'fontWeight' : 'bold'}),width = {'offset': 0})
                        ])
            ],
        ),style = {'backgroundColor' : '#141414'})),
        dbc.Col(dbc.Card(dbc.CardBody(
            [
                html.P("Average Visibility", style = {'textAlign' : 'center', 'color': 'white', 'font-size': 13}),
                dbc.Row([dbc.Col(html.I(className="fas fa-eye-slash fa-lg", style={'color': 'purple'}),width = {'size': 1, 'offset': 1}),
                    dbc.Col(html.H4(f"{round(accidents2020['Visibility(mi)'].mean(),2)} mi", style = {'color' : 'purple',
                                                                                               'textAlign' : 'center',
                                                                                                'fontWeight' : 'bold'}),width = {'offset': 0})
                        ])
            ],
        ),style = {'backgroundColor' : '#141414'})),
        dbc.Col(dbc.Card(dbc.CardBody(
            [
                html.P("Average Wind Speed", style = {'textAlign' : 'center', 'color': 'white', 'font-size': 13}),
               dbc.Row([dbc.Col(html.I(className="fas fa-wind fa-lg", style={'color': 'yellow'}),width = {'size': 2, 'offset': 1}),
                    dbc.Col(html.H4(f"{round(accidents2020['Wind_Speed(mph)'].mean(),2)} mph", style = {'color' : 'yellow',
                                                                                               'textAlign' : 'center',
                                                                                                'fontWeight' : 'bold'}),width = {'offset': 0})
                        ])
            ],
        ),style = {'backgroundColor' : '#141414', "margin-right": "15px"})),
    ]),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([dcc.Dropdown(id = 'select_city',
                                  options =[{"label": i, "value": i}for i in accidents2020['State Full Name'].unique()],
                                                       value = 'Michigan'),
                            html.Br(),
                            dcc.Graph(id ='pie', figure ='figure')]),style = {'backgroundColor' : '#141414', "margin-left": "15px"}), width = 4),
             
            dbc.Col(dbc.Card(dbc.CardBody([dbc.Row([dbc.Col([dcc.Dropdown(id = 'select_time_type',
                                  options =[{"label": "Days", "value": 'day'},
                                           {"label": "Months", "value": 'month'}],
                                              value = 'month')]),
                                  dbc.Col([dcc.Dropdown(id = 'select_category',
                                  options =[{"label": "Weather", "value": 'Weather_Condition'},
                                           {"label": "Time", "value": 'Sunrise_Sunset'}],
                                              value = 'Sunrise_Sunset',
                                           # style = {'backgroundColor' : '#3BB9FF', 'textColor': 'white'} (add color to dcc)
                                                       )])]),
                                html.Br(),
                                dcc.Graph(id = 'bar', figure = 'figure')]),style = {'backgroundColor' : '#141414', "margin-right": "15px"}), width =8)
            ]),
    html.Br(),
    dbc.Row(dbc.Col(dbc.Button('Switch Graph', id = 'button',color ='info', n_clicks=0, style = {"margin-left": "15px"}))),
    html.Br(),
    dbc.Row([dbc.Col(dcc.Graph(id = 'switched_graph', figure = 'figure', style = {"margin-left": "15px", "margin-right": "15px", "margin-bottom": "15px"}))])
    ])
@app.callback(
    Output(component_id = 'pie', component_property = 'figure'),
    Output(component_id = 'bar', component_property = 'figure'),
    Output(component_id = 'switched_graph', component_property = 'figure'),
    [Input(component_id = 'select_city', component_property = 'value'),
     Input(component_id = 'select_time_type', component_property = 'value'),
     Input(component_id = 'select_category', component_property = 'value'),
     Input(component_id = 'button', component_property = 'n_clicks')]
)
def option(selection, time, category, n):
    acc = accidents2020[accidents2020['State Full Name'] == selection]
    fig = px.pie(acc, names = acc['Weather_Condition'].value_counts().head().index,
       values = acc['Weather_Condition'].value_counts().head().values,
      hole = 0.6,
      title = f'<b>Top 5 Weather Condition Favorable For Accidents in {selection}')
    fig.update_layout(title_font_size=10,
                      title_font_color = 'white',
                     #showlegend = False,
                     template = 'plotly_dark',
                     legend=dict(
                         orientation="h",
                    ))
    #fig.update_traces(textinfo = "label+value")
    g = acc.groupby([time, category]).sum()
    fig1 = px.bar(x = g.index.get_level_values(0), y = g['accident_count'], color = g.index.get_level_values(1),
                 template = 'plotly_dark')
    fig1.update_layout(title = 'Accident Counts based on Time and Weather',
                      title_font_size=12,
                      title_font_color = 'White',
                     xaxis_title = f'{time}',
                     yaxis_title = 'Total Accidents',
                      height = 450)
    if n%2 == 0 :
        fig2 = px.choropleth(accident_count_state_wise,
                            locations = accident_count_state_wise.index.get_level_values(0),
                            locationmode = 'USA-states',
                            color = 'accident_count',
                            scope = 'usa',
                            hover_name = accident_count_state_wise.index.get_level_values(1),
                            title="<b>TOTAL ACCIDENTS OCCURED IN STATE</b>",
                            color_continuous_scale=["yellow", "orange", "brown"],
                            template = 'plotly_dark',
                             height =550,
                            labels = accident_count_state_wise.index.get_level_values(1))
        fig2.update_layout(#paper_bgcolor="pink",
            #coloraxis_showscale = False,
            coloraxis_colorbar=dict(
                title="Accident Counts"),
            margin={"r":0,"t":100,"l":0,"b":0},
            title_x=0.5)
    else:
        accident_count_city_wise = accidents2020.groupby(['State Full Name', 'City',]).sum()
        fig2 = px.treemap(accident_count_city_wise,
                    path =[accident_count_city_wise.index.get_level_values(0),
                           accident_count_city_wise.index.get_level_values(1)],
                    values="accident_count",
                    title="<b>TOTAL ACCIDENTS OCCURED IN STATE AND ITS CITY</b>",
                         template= 'plotly_dark',
                         height = 600)
        fig2.update_layout(title_x=0.5)
        fig2.update_traces(textinfo = "label+text+value")
    return fig, fig1, fig2
if __name__ =='__main__':
    app.run_server(port = 4050)