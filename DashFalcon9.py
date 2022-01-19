# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options=[
                                    {'label':'All Sites','value':'ALL'},
                                    {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                    {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                    {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                    {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}
                                ],
                                value='ALL',
                                placeholder='Select a Launch Site here',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000,
                                marks={0:'0 kg',
                                500:'500 kg',
                                1000:'1000 kg',
                                1500:'1500 kg',
                                2000:'2000 kg',
                                5000:'5000 kg',
                                7500:'7500 kg',
                                10000:'10000 kg'},                            
                                value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        rowSuccess = spacex_df['class']==0
        filtered_df = spacex_df[rowSuccess]
        fig = px.pie(filtered_df, values=None, 
        names='Launch Site', 
        title='Total Successful Launches by Site')
        return fig
    else:
        rowSite = spacex_df['Launch Site']==entered_site
        filtered_df = spacex_df[rowSite]
        fig = px.pie(filtered_df, values=None, 
        names='class', 
        title='Launch Success Rate for the Site '+entered_site,
        color = 'class',
        color_discrete_map={0:'green',1:'red'})
        return fig        
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def scatter_chart(entered_site,slider_input):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        rowPayload = (spacex_df['Payload Mass (kg)']>slider_input[0])&(spacex_df['Payload Mass (kg)']<slider_input[1])
        filtered_df = spacex_df[rowPayload]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',y='class',color='Booster Version Category') 
        return fig
    else:
        rowPayloadSite = (spacex_df['Payload Mass (kg)']>slider_input[0])&(spacex_df['Payload Mass (kg)']<slider_input[1])&(spacex_df['Launch Site']==entered_site)
        filtered_df = spacex_df[rowPayloadSite]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)',y='class',color='Booster Version Category')
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
