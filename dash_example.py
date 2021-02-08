#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: jaime
"""

import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

#fonte de dados
happiness = pd.read_csv('/python_dash/world_happiness.csv')

#componentes de seleção de dados
country_options = [{'label': i,'value':i} for i in happiness['country'].unique()]

region_options = [{'label': i,'value':i} for i in happiness['region'].unique()]

data_options = [{'label':'Happines Score','value':'happiness_score'},
                {'label':'Happines Rank','value':'happiness_rank'}]

app=dash.Dash()

#Estrutura da página exibida
app.layout=html.Div(children = [
    html.H1('World Happines Dashboard'),
    html.P(['This dashboard shows the happines score.',
            html.Br(),
            html.A('World Happines Report Data Source',
                   href='https://worldhappiness.report/',
                   target='_blank')]),
    dcc.RadioItems(id='region-radio',options=region_options,value='Latin America and Caribbean'),
    dcc.Dropdown(id='country-dropdown',options=country_options),
    dcc.RadioItems(id='data-radio',options=data_options,value='happiness_score'),
    dcc.Graph(id='happiness-graph'),
    html.Div(id='average-div')
    ])


#filtrar apenas países da região escolhida
@app.callback(
    Output('country-dropdown','options'),
    Output('country-dropdown','value'),
    Input('region-radio','value')
    )
def update_dropdown(selected_region):
    filtered_happiness=happiness[happiness['region']==selected_region]
    country_options=[{'label':i,'value':i} for i in filtered_happiness['country'].unique()]
    return country_options,country_options[0]['value']

#filtrar países e mostrar o gráfico
@app.callback(
    Output('happiness-graph','figure'),
    Output('average-div','children'),
    Input('country-dropdown', 'value'),
    Input('data-radio','value')
    )
def update_graph(selected_country, selected_data):
    filtered_happiness=happiness[happiness['country']==selected_country]
    line_fig = px.line(filtered_happiness,
                       x='year',y=selected_data,
                       title=f'{selected_data} in {selected_country}')
    selected_avg=filtered_happiness[selected_data].mean()
    return line_fig,f'The Average {selected_data} for {selected_country} is '\
                    f'{selected_avg}'

#executar servidor        
if __name__=='__main__':
    app.run_server(debug=True)
