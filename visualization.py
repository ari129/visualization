import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table, Dash
from dash.dependencies import Input, Output

# Read the files
winners = pd.read_csv('winners_clean.csv')
goalscorers = pd.read_csv('goalscorers_cleaned.csv')
scorer_worldcup = pd.read_csv('scorer_worldcup.csv')
summary_results = pd.read_csv('summary_combined.csv')


# Create the summary table for the first chart
summary_table = winners.groupby("Winner", as_index=False).agg(
    World_Cups_Won=('Year', 'count')
).rename(columns={"Winner": "Country"}).sort_values("World_Cups_Won", ascending=False)

# Calculate how many world cups were won at home
home_wins = winners[winners['Country'] == winners['Winner']].groupby('Winner').size()
summary_table["World_Cups_Won_at_Home"] = summary_table["Country"].map(home_wins).fillna(0).astype(int)

# Winner and Top Scorer for each World Cup (for second chart)
winners_per_year = winners[['Year', 'Winner']]
top_scorers = scorer_worldcup.groupby("Year").apply(
    lambda x: x.loc[x['Goals'].idxmax()]
).reset_index(drop=True)

top_scorers = top_scorers[['Year', 'Name', 'Goals', 'Country']].rename(
    columns={
        'Name': 'Top_Scorer',
        'Goals': 'Goals_Scored',
        'Country': 'Country'
    }
)

world_cup_summary = pd.merge(winners_per_year, top_scorers, on="Year")
world_cup_summary = world_cup_summary[['Year', 'Winner', 'Top_Scorer', 'Goals_Scored']]

# Contar cuántos mundiales ha ganado cada país
world_cup_wins = winners['Winner'].value_counts().reset_index()
world_cup_wins.columns = ['Country', 'Total_Wins']

# Crear una tabla resumen
summary_table = winners.groupby("Winner", as_index=False).agg(
    World_Cups_Won=('Year', 'count')
).rename(columns={"Winner": "Country"}).sort_values("World_Cups_Won", ascending=False)

# Calcular cuántos mundiales ganó cada país en casa
home_wins = winners[winners['Country'] == winners['Winner']].groupby('Winner').size()
summary_table["World_Cups_Won_at_Home"] = summary_table["Country"].map(home_wins).fillna(0).astype(int)

# Calcular total de goles por país
total_goals_by_country = goalscorers \
    .groupby("team", as_index=False) \
    .sum("goals") \
    .rename(columns={"goals": "total_goals"}) \
    .sort_values("total_goals", ascending=False)
    
# Winner for each World Cup
winners_per_year = winners[['Year', 'Winner']]

image_map = {
    "Guillermo Stábile": "stabile.png",
    "Oldřich Nejedlý": "nejedly.png",
    "Leônidas da Silva": "leonidas.png",
    "Ademir": "ademir.png",
    "Sandor Kocsis": "kocsis.png",
    "Just Fontaine": "fontaine.png",
    "Garrincha": "garrincha.png",
    "Vavá": "vava.png",
    "Flórián Albert": "albert.png",
    "Valentin Ivanov": "ivanov.png",
    "Dražan Jerković": "jerkovic.png",
    "Leonel Sánchez": "sanchez.png",
    "Eusébio": "eusebio.png",
    "Gerd Müller": "muller.png",
    "Grzegorz Lato": "lato.png",
    "Mario Alberto Kempes": "kempes.png",
    "Paolo Rossi": "rossi.png",
    "Gary Lineker": "lineker.png",
    "Salvatore Schillaci": "schillaci.png",
    "Oleg Salenko": "salenko.png",
    "Hristo Stoitchkov": "stoitchkov.png",
    "Davor Šuker": "suker.png",
    "Ronaldo": "ronaldo.png",
    "Miroslav Klose": "klose.png",
    "Thomas Müller": "muller.png",
    "David Villa": "villa.png",
    "Wesley Sneijder": "sneijder.png",
    "Diego Forlán": "forlan.png",
    "James Rodríguez": "james.png",
    "Harry Kane": "kane.png",
    "Kylian Mbappé": "mbappe.png"
}

def goles_por_pais(data):
    goles_df = data.groupby('Year')['QualifiedTeams'].sum().reset_index()
    fig = px.scatter(goles_df, x='Year', y='QualifiedTeams', title='Qualified Teams')
    return fig

# Gráfico 2: Asistencia por año
def asistencia_por_ano(data):
    asistencia_df = data.groupby('Year')['Attendance'].sum().reset_index()
    fig = px.line(asistencia_df, x='Year', y='Attendance', markers=True, title='Attendance')
    return fig

# Gráfico 3: Equipos clasificados vs partidos jugados
def equipos_vs_partidos(data):
    equipos_df = data.groupby('Year')[ 'MatchesPlayed'].sum().reset_index()
    fig = px.scatter(equipos_df, x='Year', y='MatchesPlayed', title='Matches Played')
    return fig

# Gráfico 4: Posiciones finales
def posiciones_finales(data):
    df_pos = data[['Winner', 'RunnersUp', 'Third', 'Fourth']].melt(value_name='Country', var_name='Position')
    posiciones_df = df_pos.groupby(['Country', 'Position']).size().unstack(fill_value=0).reset_index()
    fig = px.bar(posiciones_df, x='Country', y=['Winner', 'RunnersUp', 'Third', 'Fourth'],
                 title='Final positions', labels={'value': 'Quantity', 'Country': 'Country'})
    return fig




# Crear la aplicación Dash
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.Div([
        html.Img(
            src=app.get_asset_url('image1.png'),
            style={
                'width': '50%',  
                'height': 'auto',  
                'display': 'block',
                'margin': '0 auto'
            }
        )
    ], style={'text-align': 'center', 'margin-bottom': '20px'}),
    html.H1("ANALYSIS OF THE WORLD CUP", style={'text-align': 'center'}),
    html.Div(
        html.P(
        "Welcome to all football enthusiasts! In this page, we can analyze the evolution of the World Cup over the years. "
        "You will be able to interact with this page and explore various insights! "
        "At the beginning, you will find an interactive map where you can view the results from the first match for each nation, "
        "including the number of wins, losses, and home wins. By clicking on a country, you can access detailed information about its performance! "
        "Additionally, you can explore other graphs that provide deeper insights into the tournaments, such as goals scored by each country, "
        "attendance over the years, the number of teams qualified, and the final positions in the competition. "
        "Feel free to filter by years and countries to customize the analysis to your interests. "
        "This is your chance to dive into the history of the World Cup and analyze how the competition has evolved over time."
        ),
        style={
            'max-width': '800px',  
            'margin': '0 auto',    
            'text-align': 'center', 
            'padding': '20px'       
        }
    ),

    # Sección del dropdown y el mapa
    html.Div([
        html.H3("Select Metric for the Map:", style={'text-align': 'center'}),
        dcc.Dropdown(
            id='metric_dropdown',
            options=[
                {'label': 'Wins', 'value': 'Wins'},
                {'label': 'Losses', 'value': 'Losses'},
                {'label': 'Home Wins', 'value': 'Home Wins'}
            ],
            value='Wins',  # Métrica por defecto
            style={'width': '50%', 'margin': '0 auto'}
        )
    ], style={'margin-bottom': '30px'}),
    
    # Resumen del país seleccionado
    html.Div([
        html.H3("Country Summary", style={'text-align': 'center'}),
        html.Div(id='country_summary', style={'text-align': 'center', 'margin': '20px'})
    ]),

    
   html.Div([
        dcc.Graph(id='choropleth_map', style={'height': '80vh'})
    ]), 

        # Bar chart for world cups won
    html.Div([
            html.H3("World Cups Won and Won at Home", style={'text-align': 'center'}),
            dcc.Graph(id='bar_chart', style={'height': '600px', 'width': '100%'})  # Adjust chart size
        ]),
    
        # Visualization for second table
    html.Div([
    html.H3("Top Scorers of the World Cup", style={'text-align': 'center'}),
    html.Div([
        dcc.Graph(
            id='line_chart',
            style={"height": "70vh", "width": "70%"}  # Ajusta el tamaño del gráfico
        ),
        html.Div(
            id="player_image_container",
            style={
                "width": "30%",  # El resto del espacio es para la imagen
                "marginLeft": "20px",  # Espaciado entre el gráfico y la imagen
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center"
            }
        )
    ], style={
        "display": "flex",
        "flexDirection": "row",  # Asegura que estén en fila
        "alignItems": "center",
        "justifyContent": "space-between",
        "marginTop": "20px"
    }),  # Contenedor principal como flex
]),
    html.Div([
    html.H1("Evolution of the World Cup", style={'text-align': 'center'}),
    
    # Filtros para los años y países
    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in sorted(winners['Year'].unique())],
            multi=True,
            placeholder="Choose year(s)",
            style={'text-align': 'center'},
        ),
        
    ],  style={'text-align': 'center'}),
    
    # Gráficos organizados en dos filas
    html.Div([
        # Fila superior (2 gráficos)
        html.Div([
            dcc.Graph(id='Attendance', style={'width': '48%', 'height': '400px', 'display': 'inline-block'}),
            dcc.Graph(id='Final positions', style={'width': '48%', 'height': '400px', 'display': 'inline-block'})
        ], style={'display': 'flex', 'justify-content': 'space-between'}),
        
        # Fila inferior (2 gráficos)
        html.Div([
            dcc.Graph(id='Matches played', style={'width': '48%', 'height': '400px', 'display': 'inline-block'}),
            dcc.Graph(id='Qualified teams', style={'width': '48%', 'height': '400px', 'display': 'inline-block'})
        ], style={'display': 'flex', 'justify-content': 'space-between'}),
    ])
])

])


# Callback para actualizar el gráfico según el país seleccionado
@app.callback(
    Output('choropleth_map', 'figure'),
    [Input('metric_dropdown', 'value')]
)

def update_map(selected_metric):
    # Crear el gráfico de coropletas
    fig = px.choropleth(
        summary_results,
        locations="Country",
        locationmode="country names",
        color=selected_metric,
        hover_name="Country",
        title=f"Selection: {selected_metric}",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    return fig

@app.callback(
    Output('country_summary', 'children'),
    [Input('choropleth_map', 'clickData')]
)
def update_country_summary(clickData):
    if clickData is None:
        return "Click on a country to see the summary."

    # Obtener el país seleccionado
    country = clickData['points'][0]['location']

    # Filtrar los datos según el país
    country_data = summary_results[summary_results['Country'] == country]

    if country_data.empty:
        return f"No data available for {country}."

    # Extraer los valores necesarios
    matches_played = country_data['Matches Played'].values[0]
    wins = country_data['Wins'].values[0]
    losses = country_data['Losses'].values[0]
    home_wins = country_data['Home Wins'].values[0]
    world_cups_won = country_data['World Cups Won'].values[0]
    world_cup_locations = country_data['World Cup Locations'].values[0]
    shootout_wins = country_data['Shootout Wins'].values[0]

    # Crear el resumen en formato HTML
    return html.Div([
        html.P(f"Matches Played: {matches_played}"),
        html.P(f"Wins: {wins}"),
        html.P(f"Losses: {losses}"),
        html.P(f"Home Wins: {home_wins}"),
        html.P(f"World Cups Won: {world_cups_won}"),
        html.P(f"World Cup Locations: {world_cup_locations}"),
        html.P(f"Shootout Wins: {shootout_wins}")
    ])


@app.callback(
    Output('bar_chart', 'figure'),
    [Input('bar_chart', 'id')]
)
def update_bar_chart(_):
    fig = px.bar(
        summary_table,
        x="Country",
        y=["World_Cups_Won", "World_Cups_Won_at_Home"],
        barmode="group",
        labels={"value": "World Cups", "variable": "Category"},
        title="World Cups Won and Won at Home",
        text_auto=True
    )
    fig.update_layout(
        legend=dict(title="Category", orientation="h", x=0.5, xanchor="center", y=1.1),
        xaxis_title="Country",
        yaxis_title="Number of World Cups",
    )
    return fig


@app.callback(
    Output('line_chart', 'figure'),
    [Input('line_chart', 'id')]
)
def update_line_chart(_):
    fig = px.scatter(
        top_scorers,
        x="Year",
        y="Goals_Scored",
        color="Country", 
        hover_data={"Top_Scorer": True, "Country":True},
        title="Top Scorers and Goals Scored by Year",
        labels={"Goals_Scored": "Goals Scored", "Year": "World Cup Year"},
        text="Top_Scorer"
    )
    fig.update_traces(marker=dict(size=12), textposition="top center")
    return fig


@app.callback(
    Output('player_image_container', 'children'),
    [Input('line_chart', 'clickData')]
)
def display_player_image(click_data):
    if click_data is None:
        return "Click on a point to see the player's photo."

    # Extraer la información del clic
    point = click_data["points"][0]
    top_scorer = point["text"]  # El texto del punto (Top Scorer)
    image_url = image_map.get(top_scorer, None)

    if image_url:
        return html.Img(
            src=app.get_asset_url(image_url),
            style={"width": "300px", "borderRadius": "10px"}
        )

    return f"No image available for {top_scorer}."


@app.callback(
    Output('Attendance', 'figure'),
    Output('Final positions', 'figure'),
    Output('Matches played', 'figure'),
    Output('Qualified teams', 'figure'),
    Input('year-dropdown', 'value'),
)
def update_graphs(selected_years):
    # Filtro de años
    filtered_data = winners
    if selected_years:
        filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]

    # Actualizar gráficos con los datos filtrados
    goles_fig = goles_por_pais(filtered_data)
    asistencia_fig = asistencia_por_ano(filtered_data)
    equipos_fig = equipos_vs_partidos(filtered_data)
    posiciones_fig = posiciones_finales(filtered_data)

    return goles_fig, asistencia_fig, equipos_fig, posiciones_fig



# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)


# Agrupar los goles por equipo
total_goals_by_country = goalscorers \
    .groupby("team", as_index=False) \
    .sum("goals") \
    .rename(columns={"goals": "total_goals"}) \
    .sort_values("total_goals", ascending=False)

# Crear el gráfico de coropletas
fig = px.choropleth(total_goals_by_country, 
                    locations="team",
                    locationmode="country names",
                    color="total_goals",
                    hover_name="team",
                    title="Goals of the maximun scorer of each country")
fig.show()