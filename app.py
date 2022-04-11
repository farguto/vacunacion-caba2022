#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Instalación de librerías 

#!pip install jupyter-dash
#!pip install dash
#!pip install dash_core_components
#!pip install dash_html_components
#!pip install dash_table
#!pip install dash_bootstrap_components




# Importamos librerías


import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

datos = pd.read_csv("https://cdn.buenosaires.gob.ar/datosabiertos/datasets/salud/plan-de-vacunacion-covid-19/dataset_total_vacunas.csv")


datos = datos.drop('ID_CARGA', axis=1)

# Primeras Dosis aplicadas
pregunta1 = datos.DOSIS_1.sum()


# Segundas Dosis aplicadas
pregunta2 = datos.DOSIS_2.sum()

# Terceras Dosis aplicadas
pregunta2b = datos.DOSIS_3.sum()


# Total de vacunas aplicadas en la Ciudad
pregunta3 = datos['DOSIS_1'].sum()+datos['DOSIS_2'].sum()

# Cantidad de primeras dosis por tipo de establecimiento
pregunta4 = datos.groupby('TIPO_EFECTOR').sum()
pregunta4 = pregunta4.assign(TIPO_EFECTOR=pregunta4.index)
pregunta4 = pregunta4.sort_values('DOSIS_1', ascending=False)
pregunta4 = pregunta4.reindex(columns=['TIPO_EFECTOR', 'DOSIS_1'])

# Cantidad de segundas dosis por tipo de establecimiento
pregunta4b = datos.groupby('TIPO_EFECTOR').sum()
pregunta4b = pregunta4b.assign(TIPO_EFECTOR=pregunta4b.index)
pregunta4b = pregunta4b.sort_values('DOSIS_2', ascending=False)
pregunta4b = pregunta4b.reindex(columns=['TIPO_EFECTOR', 'DOSIS_2'])

# Cantidad de Terceras dosis por tipo de establecimiento
pregunta4c = datos.groupby('TIPO_EFECTOR').sum()
pregunta4c = pregunta4c.assign(TIPO_EFECTOR=pregunta4c.index)
pregunta4c = pregunta4c.sort_values('DOSIS_3', ascending=False)
pregunta4c = pregunta4c.reindex(columns=['TIPO_EFECTOR', 'DOSIS_3'])




#Cantidad de primeras dosis aplicadas por tipo de vacuna
pregunta5 = datos.groupby('VACUNA').sum()
pregunta5 = pregunta5.assign(VACUNA=pregunta5.index)
pregunta5 = pregunta5.sort_values('DOSIS_1', ascending=False)
pregunta5 = pregunta5.drop(['DOSIS_2'], axis=1)
pregunta5 = pregunta5.reindex(columns=['VACUNA', 'DOSIS_1'])

#Cantidad de segundas dosis aplicadas por tipo de vacuna
pregunta5b = datos.groupby('VACUNA').sum()
pregunta5b = pregunta5b.assign(VACUNA=pregunta5b.index)
pregunta5b = pregunta5b.sort_values('DOSIS_2', ascending=False)
pregunta5b = pregunta5b.drop(['DOSIS_1'], axis=1)
pregunta5b = pregunta5b.reindex(columns=['VACUNA', 'DOSIS_2'])

#Cantidad de terceras dosis aplicadas por tipo de vacuna
pregunta5c = datos.groupby('VACUNA').sum()
pregunta5c = pregunta5c.assign(VACUNA=pregunta5c.index)
pregunta5c = pregunta5c.sort_values('DOSIS_3', ascending=False)
pregunta5c = pregunta5c.drop(['DOSIS_1'], axis=1)
pregunta5c = pregunta5c.reindex(columns=['VACUNA', 'DOSIS_3'])


# Cantidad de vacunas aplicadas por grupto etario

pregunta6 = datos.groupby('GRUPO_ETARIO').sum()
pregunta6 = pregunta6.assign(GRUPO_ETARIO=pregunta6.index)
pregunta6 = pregunta6.reindex(columns=['GRUPO_ETARIO', 'DOSIS_1', 'DOSIS_2', 'DOSIS_3'])


# Cantidad de vacunas aplicadas por género
pregunta7 = datos.groupby('GENERO').sum()
pregunta7 = pregunta7.assign(GENERO=pregunta7.index)
pregunta7 = pregunta7.reindex(columns=['GENERO', 'DOSIS_1', 'DOSIS_2', 'DOSIS_3'])

#Los 5 días que se aplicaron mayor cantidad de primeras dosis

datos2 = datos.groupby('FECHA_ADMINISTRACION').sum()
datos2 = datos2.sort_values(by= 'DOSIS_1', ascending=False)
datos2 = datos2.drop('DOSIS_2', axis=1)
pregunta8 = datos2.head(5)
pregunta8 = pregunta8.assign(FECHA_ADMINISTRACION=pregunta8.index)
pregunta8 = pregunta8.reindex(columns=['FECHA_ADMINISTRACION', 'DOSIS_1'])



#Los 5 días que se aplicaron mayor cantidad de segundas dosis
datos2 = datos.groupby('FECHA_ADMINISTRACION').sum()
datos2 = datos2.sort_values(by= 'DOSIS_2', ascending=False)
datos2 = datos2.drop('DOSIS_1', axis=1)
pregunta9= datos2.head(5)
pregunta9 = pregunta9.assign(FECHA_ADMINISTRACION=pregunta9.index)
pregunta9 = pregunta9.reindex(columns=['FECHA_ADMINISTRACION', 'DOSIS_2'])



#Los 5 días que se aplicaron mayor cantidad de terceras dosis
datos3 = datos.groupby('FECHA_ADMINISTRACION').sum()
datos3 = datos3.sort_values(by= 'DOSIS_3', ascending=False)
datos3 = datos3.drop('DOSIS_1', axis=1)
pregunta10= datos3.head(5)
pregunta10 = pregunta10.assign(FECHA_ADMINISTRACION=pregunta10.index)
pregunta10 = pregunta10.reindex(columns=['FECHA_ADMINISTRACION','DOSIS_3'])


# Porcentaje estimado de vacunados con dos dosis en Caba
poblacion_estimada_caba = 3075646
porcentaje_vacunados = (pregunta2*100)/poblacion_estimada_caba
porcentaje_vacunados = porcentaje_vacunados.round(2)

#App


#se inicia la App y se le agrega una selección de un tema en bootstrap.



external_stylesheets = [
   
    'assets/style.css', 'http://fonts.googleapis.com/css?family=Roboto', dbc.themes.SPACELAB

]


app=dash.Dash(__name__, external_stylesheets=external_stylesheets)


#Server
server = app.server




#Layout
app.layout = html.Div([
    html.H1('Monitor de vacunación en la Ciudad Autónoma de Buenos Aires'), 
    html.H6('Datos Abiertos tomados del Gobierno de la Ciudad'),




    # Dentro de dcc.Tabs se colocan los 2 tabs.

# En Tab1 se inserta un mapa de Campanas Verdes y Puntos Verdes mediante la utilización de un Iframe, en el cual se encuentra el mapa en html. 

    dcc.Tabs([


       
        dcc.Tab(id='Tab1', label='La vacunación en gráficos',  children=[

        html.Div([

            html.Div([

                 dcc.RadioItems(id = 'dosis-radio',
                            labelStyle= {'display':'inline-block'}, 
                            options = [
                                {'label': 'Primera dosis', 'value': 'DOSIS_1'},
                                {'label': 'Segunda dosis', 'value': 'DOSIS_2'},
                                {'label': 'Tercera dosis', 'value': 'DOSIS_3'}
                            ], value = 'DOSIS_1' , 
                           
                           ),

            ]),         
        ]),

        
            html.Div([
                    dcc.Graph(id = 'grafico_vacunas', figure = {})

            ]),

        html.Div([

        dcc.Dropdown(id="dropdown_edad",
       
        options=[
            {'label': 'Primera Dosis por edad', 'value': 'DOSIS_1'},
            {'label': 'Segunda Dosis por edad', 'value': 'DOSIS_2'},
            {'label': 'Tercera Dosis por edad', 'value': 'DOSIS_3'},
        ],
        value='DOSIS_1',
        multi=False,
       
        )
        

        ]),

         
            html.Div([
                    dcc.Graph(id = 'grafico2', figure = {})

            ]),

        

        ]),



            
        dcc.Tab(id='Tab2', label='La vacunación en números',  children=[   

            html.Div([                           
    
            html.P('Población vacunada en CABA con primera dosis: '+ str(pregunta1),),

            html.P('Población vacunada en CABA con segunda dosis: '+ str(pregunta2),),

            html.P('Población vacunada en CABA con tercera dosis: '+ str(pregunta2b),),

            html.P('Total de vacunas aplicadas en CABA: '+ str(pregunta3),),

            html.P('Porcentaje estimado de vacunados con el esquema completo (dos dosis): '+ str(porcentaje_vacunados),),
            
            ]),
  
            html.Div([  
            html.P( 'Cantidad de primeras dosis por tipo de establecimiento: '),

            
            
            dash_table.DataTable(
                id='tabla_pregunta4',
                columns=[
                        {"name": "Tipo de establecimiento", "id": "TIPO_EFECTOR"},
                        {"name": "Primera Dosis", "id": "DOSIS_1"},],
                data=pregunta4.to_dict('records'),
                
                    style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300},
                    style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300}, 
            
                filter_action='native', 
                page_current= 0,
                page_size= 10,
                
            ),
            ]),

            html.Br(),   
            html.Br(),
            html.Br(),
            html.Br(),
        
            html.Div([ 
            html.P( 'Cantidad de segundas dosis por tipo de establecimiento: '),

            dash_table.DataTable(
                id='tabla_pregunta4b',
                columns=[
                        {"name": "Tipo de establecimiento", "id": "TIPO_EFECTOR"},
                        {"name": "Segunda Dosis", "id": "DOSIS_2"},],
                data=pregunta4b.to_dict('records'),
         
                   style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300},
                   style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300}, 
                filter_action='native', 
                page_current= 0,
                page_size= 10,
                ),

                ]),


            html.Div([ 
            html.P( 'Cantidad de terceras dosis por tipo de establecimiento: '),

            dash_table.DataTable(
                id='tabla_pregunta4c',
                columns=[
                        {"name": "Tipo de establecimiento", "id": "TIPO_EFECTOR"},
                        {"name": "Tercera Dosis", "id": "DOSIS_3"},],
                data=pregunta4c.to_dict('records'),
         
                   style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300},
                   style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300}, 
                filter_action='native', 
                page_current= 0,
                page_size= 10,
                ),

                ]),



                html.Div([ 
                html.P( 'Primeras dosis aplicadas por tipo de vacuna: '),
                dash_table.DataTable(
                    id='tabla_pregunta5',
                    columns=[
                    {"name": "Vacuna", "id": "VACUNA"},
                    {"name": "Primera Dosis", "id": "DOSIS_1"},],
                    data=pregunta5.to_dict('records'),
        
                    style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 400, 'maxWidth': 400, 'width': 400},
                    style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 400, 'maxWidth': 400, 'width': 400}, 
                    filter_action='native', 
                    page_current= 0,
                    page_size= 10,
                ),
                ]),

                html.Div([ 
                html.P( 'Segundas dosis aplicadas por tipo de vacuna: '),
                dash_table.DataTable(
                    id='tabla_pregunta5b',
                    columns=[
                    {"name": "Vacuna", "id": "VACUNA"},
                    {"name": "Segunda dosis", "id": "DOSIS_2"},],
                    data=pregunta5b.to_dict('records'),

                    style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 400, 'maxWidth': 400, 'width': 400},
                    style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 400, 'maxWidth': 400, 'width': 400},      
                    filter_action='native', 
                    page_current= 0,
                    page_size= 10,
                ),
                ]),
                
                html.Div([ 
                html.P( 'Terceras dosis aplicadas por tipo de vacuna: '),
                dash_table.DataTable(
                    id='tabla_pregunta5c',
                    columns=[
                    {"name": "Vacuna", "id": "VACUNA"},
                    {"name": "Tercera dosis", "id": "DOSIS_3"},],
                    data=pregunta5c.to_dict('records'),

                    style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 400, 'maxWidth': 400, 'width': 400},
                    style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 400, 'maxWidth': 400, 'width': 400}, 
                    filter_action='native', 
                    page_current= 0,
                    page_size= 10,
                ),
                ]),
                     
        
        
                html.Div([
                html.P( 'Cantidad de vacunas aplicadas por grupo etario: '),
                dash_table.DataTable(
                    id='tabla_pregunta6',
                    columns=[
                    {"name": "Grupo Etario", "id": "GRUPO_ETARIO"},
                    {"name": "Primera dosis", "id": "DOSIS_1"},
                    {"name": "Segunda dosis", "id": "DOSIS_2"},
                    {"name": "Tercera dosis", "id": "DOSIS_3"},],
                    data=pregunta6.to_dict('records'),
                
                    style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 200, 'maxWidth': 200, 'width': 200},
                    style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 200, 'maxWidth': 200, 'width': 200}, 
                    filter_action='native', 
                    page_current= 0,
                    page_size= 10,
                    ),
                ]),
        
        
                html.Div([
                html.P( 'Los 5 días que se aplicaron mayor cantidad de primeras dosis: '),
                dash_table.DataTable(
                    id='tabla_pregunta8',
                    columns=[
                                  
                        {"name": "Fecha de Administración", 
                        "id": "FECHA_ADMINISTRACION" ,
                                     
                    },
                    {"name": "Primeras Dosis", "id": "DOSIS_1"},],
                    data=pregunta8.to_dict('records'),
                    style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300},
                    style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300}, 
                    filter_action='native', 
                    page_current= 0,
                    page_size= 10,
                ),
                ]),


                html.Div([
                html.P( 'Los 5 días que se aplicaron mayor cantidad de segundas dosis: '),
                dash_table.DataTable(
                    id='tabla_pregunta9',
                    columns=[
                    {"name": "Fecha de Administración", "id": "FECHA_ADMINISTRACION"},
                    {"name": "Segundas Dosis", "id": "DOSIS_2"},],
                    data=pregunta9.to_dict('records'),
                    style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300},
                    style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300}, 
                    filter_action='native', 
                    page_current= 0,
                    page_size= 10,
                ),
                ]),

                html.Div([
                html.P( 'Los 5 días que se aplicaron mayor cantidad de terceras dosis: '),
                dash_table.DataTable(
                    id='tabla_pregunta10',
                    columns=[
                    {"name": "Fecha de Administración", "id": "FECHA_ADMINISTRACION"},
                    {"name": "Terceras Dosis", "id": "DOSIS_3"},],
                    data=pregunta10.to_dict('records'),
                    style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300},
                    style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 300, 'maxWidth': 300, 'width': 300}, 
                    filter_action='native', 
                    page_current= 0,
                    page_size= 10,
                ),
                ]),

   
                html.Div([
                html.P( 'Cantidad de vacunas aplicadas por género: '),

                dash_table.DataTable(
                    id='tabla_pregunta7',
                    columns=[
                    {"name": "Género", "id": "GENERO"},
                    {"name": "Primeras dosis", "id": "DOSIS_1"},
                    {"name": "Segundas dosis", "id": "DOSIS_2"},
                    {"name": "Terceras dosis", "id": "DOSIS_3"},],
                    data=pregunta7.to_dict('records'),
                    style_header={'backgroundColor': 'steelblue', 'color':'white', 'textAlign': 'center', 'minWidth': 150, 'maxWidth': 150, 'width': 150},
                    style_cell={'backgroundColor': 'ghostwhite', 'color': 'steelblue', 'textAlign': 'center', 'minWidth': 150, 'maxWidth': 150, 'width': 150}, 
                    filter_action='native', 
                    page_current= 0,
                    page_size= 10,
                ),
                
                ]),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),   
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),   
                    html.Br(),
                    html.H6('Desarrollado por Federico Arguto'),

     

    ]),
        
                      
    
 
    ])

])

@app.callback(
    Output('grafico_vacunas', component_property='figure'),
    [Input('dosis-radio', component_property='value')]

)

def update_graph_pie(value):

    if value == 'DOSIS_1':
        fig =  px.pie(
            data_frame= datos,
            names='VACUNA',
            values= 'DOSIS_1',
            hole=.3, 
            title='Cantidad y tipo de vacunas aplicadas en primera dosis'
        )

    elif value == 'DOSIS_2':
        fig =  px.pie(
            data_frame= datos,
            names='VACUNA',
            values= 'DOSIS_2',
            hole=.3, 
            title='Cantidad y tipo de vacunas aplicadas en segunda dosis'
        )

    else:
        fig =  px.pie(
            data_frame= datos,
            names='VACUNA',
            values= 'DOSIS_3',
            hole=.3, 
            title='Cantidad y tipo de vacunas aplicadas en tercera dosis'
        )

    return fig


@app.callback(
    Output('grafico2', component_property='figure'),
    [Input('dropdown_edad', component_property='value')]

)

def update_graph_dropdown(value):

    if value == 'DOSIS_1':
        fig2 =  px.histogram(
            data_frame= datos,
    
            x= 'DOSIS_1',
            y='GRUPO_ETARIO',
            color="GRUPO_ETARIO",
            title="Cantidad de primeras dosis aplicadas por grupo etario",
            labels={
                     "DOSIS_1": "Primeras dosis",
                     "GRUPO_ETARIO": "Grupo etario",
                    
                     
                 },

           
        )

    elif value == 'DOSIS_2':
        fig2 =  px.histogram(
            data_frame= datos,
    
            x= 'DOSIS_2',
            y='GRUPO_ETARIO',
            color="GRUPO_ETARIO",
            title="Cantidad de segundas dosis aplicadas por grupo etario",
                
            labels={
                     "DOSIS_2": "Segundas dosis",
                     "GRUPO_ETARIO": "Grupo etario",
                     
                 },
        )

    else:
        fig2 =  px.histogram(
            data_frame= datos,
    
            x= 'DOSIS_3',
            y='GRUPO_ETARIO',
            color="GRUPO_ETARIO",
            title="Cantidad de terceras dosis aplicadas por grupo etario",
                
            labels={
                     "DOSIS_3": "Terceras dosis",
                     "GRUPO_ETARIO": "Grupo etario",
                     
                 },
        )

    return fig2 

#Ejecutar
if __name__ == '__main__':
    app.run_server(port=8053)


# %%
