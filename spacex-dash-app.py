# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
server = app.server  # utile si déploiement

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # ===== TASK 1: Launch Site dropdown =====
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',  # default ALL
        placeholder="Select a Launch Site here",
        searchable=True,
        style={'width': '60%', 'margin': '0 auto'}
    ),

    html.Br(),

    # ===== TASK 2: Pie chart =====
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # ===== TASK 3: Range Slider =====
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # ===== TASK 4: Scatter chart =====
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# ===== TASK 2: Callback pie chart =====
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Total des succès (class=1) par site
        df_success = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df_success, names='Launch Site',
                     title='Total Successful Launches by Site (All Sites)')
    else:
        # Succès vs Échecs pour le site sélectionné
        df_site = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(df_site, names='class',
                     title=f'Launch Outcomes at {entered_site}', hole=0.3)
        fig.update_layout(legend_title_text='class (0=Fail, 1=Success)')
    return fig

# ===== TASK 4: Callback scatter =====
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    # Filtre par plage de payload
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                   (spacex_df['Payload Mass (kg)'] <= high)]
    # Filtre par site si nécessaire
    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]
        title = f'Payload vs. Success — {selected_site}'
    else:
        title = 'Payload vs. Success — All Sites'

    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        hover_data=['Launch Site'],
        title=title
    )
    fig.update_yaxes(tickmode='array', tickvals=[0, 1], ticktext=['Fail (0)', 'Success (1)'])
    return fig
# Run the app
if __name__ == '__main__':
    app.run()
