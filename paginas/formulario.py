from dash import Dash, dcc, html, ClientsideFunction
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import joblib
import pandas as pd
import numpy as np
import time     
from app import app


modelo = joblib.load('modelo_xgboost.pkl')
medianas = joblib.load('medianas.pkl')



titulo = html.Div(
    html.H1("Previsão de Doença Cardíaca"),
    className='titulo'
)

formulario = dbc.Container([
    html.P(
        [
            "Este projeto foi desenvolvido exclusivamente para fins acadêmicos e de portfólio em ciência de dados. "
            "As previsões geradas não possuem validade clínica e NUNCA devem ser utilizadas como base para diagnóstico ou decisão médica. "
            "ATENÇÃO: mantenha acompanhamento médico regular e não se automedique.",
            html.Br()
        ], 
        className="aviso-projeto"
    ),
    dbc.Alert(
        "Preencha as informações abaixo para que o modelo tente identificar se há ou não indícios de doença cardíaca.",
        className='identificação',
    ),
        dbc.Row([
            #coluna 1
            dbc.Col([
                #O cardGroup é como se fosse um grupinho para cada grupo e em cada grupo eu posso colocar caracteristicas para cada um
                dbc.CardGroup([
                    dbc.Label("Idade"),
                    dbc.Input(id='idade', type='number', placeholder='Digite a sua idade')
                ], class_name='mb-3'),
                dbc.CardGroup([
                    dbc.Label("Sexo Biológico"),
                        dbc.Select(id='sexo', options=[
                            {'label': 'Masculino', 'value': '1'},
                            {'label': 'Feminino', 'value': '0'}
                        ])
                ], class_name='mb-3'),
                #tipo de dor no peito
                dbc.CardGroup([
                        dbc.Label("Tipo de dor no peito"),
                            dbc.Select(id='cp', options=[
                                {'label': 'Angina típica', 'value': '1'},
                                {'label': 'Angina atípica', 'value': '2'},
                                {'label': 'Não angina', 'value': '3'},
                                {'label': 'Angina assintomática', 'value': '4'}
                            ])
                    ], class_name='mb-3'),

                #trestbps
                dbc.CardGroup([
                    dbc.Label("Pressão Arterial em Repouso"),
                    dbc.Input(id='trestbps', type='number', placeholder='Digite a sua pressão arterial em repouso')
                ], class_name='mb-3'),

                #colesterol chol
                dbc.CardGroup([
                    dbc.Label("Colesterol Sérico"),
                    dbc.Input(id='chol', type='number', placeholder="Digite o seu colesterol")
                ], class_name='mb-3'),

                #Glicemia em jejum fbs
                dbc.CardGroup([
                    dbc.Label("Glicemia em Jejum"),
                    dbc.Select(id='fbs', options=[
                        {'label': 'Menor ou igual a 120 mg/dL', 'value': '0'},
                        {'label': 'Maior que 120 mg/dL', 'value': '1'}
                    ])
                ], class_name='mb-3'),

                #eletrocardiografia em repouso resrecg
                dbc.CardGroup([
                    dbc.Label("Eletrocardiografia em repouso"),
                    dbc.Select(id='restecg', options=[
                        {'label': 'Normal', 'value': '0'},
                        {'label': 'Anormalidade de ST-T', 'value': '1'},
                        {'label': 'Hipertrofia ventricular esquerda', 'value': '2'}
                    ])
                ], class_name='mb-3'),
            ], xs=12, lg=6, className="form"),

            #coluna 2
            dbc.Col([
                #frequencia cardiaca thalach
                dbc.CardGroup([
                    dbc.Label("Frequência Cardíaca Máxima Atingida"),
                    dbc.Input(id='thalach', type='number', placeholder="Digite a sua frequência cardíaca máxima atingida")
                ], class_name='mb-3'),

                #angina atingida por exercicio exang
                dbc.CardGroup([
                    dbc.Label("Angina induzida por exercício"),
                    dbc.Select(id='exang', options=[
                        {'label': 'Sim', 'value': '1'},
                        {'label': 'Não', 'value': '0'}
                    ]),
                ], className='mb-3'),

                #depressao induzida oldpeak
                dbc.CardGroup([
                    dbc.Label("Depressão do segmento ST induzida por exercício"),
                    dbc.Input(id='oldpeak', type='number', placeholder='Digite a depressão do segmento ST induzida por exercício'),
                ], className='mb-3'),

                # slope
                dbc.CardGroup([
                    dbc.Label("Inclinação do segmento ST"),
                    dbc.Select(id='slope', options=[
                        {'label': 'Ascendente', 'value': '1'},
                        {'label': 'Plana', 'value': '2'},
                        {'label': 'Descendente', 'value': '3'}
                    ]),
                ], className='mb-3'),

                # ca
                dbc.CardGroup([
                    dbc.Label("Número de vasos principais coloridos por fluoroscopia"),
                    dbc.Select(id='ca',
                        options = [
                            { 'label': '0', 'value': '0' },
                            { 'label': '1', 'value': '1' },
                            { 'label': '2', 'value': '2' },
                            { 'label': '3', 'value': '3' },
                        ]
                    )
                ], className='mb-3'),

                # thal, cintilografia do miocardio
                dbc.CardGroup([
                    dbc.Label("Cintilografia do miocárdio"),
                    dbc.Select(id='thal', options=[
                        {'label': 'Normal', 'value': '3'},
                        {'label': 'Defeito fixo', 'value': '6'},
                        {'label': 'Defeito reversível', 'value': '7'}
                    ]),
                ], className='mb-3'),

               dbc.CardGroup([
                   dbc.Button("Prever", id='botao-prever', color='primary', n_clicks=0)
               ], class_name='area-botao') 
            ], xs=12, lg=6, className="form")
        ])
    ])

load = dcc.Loading(
        html.Div(id='previsao', style={'minHeight': '75px'}),
        type="circle",
        color="#194a7a",
        className='mt-3'
    )

rodape = html.Footer(
    [
        html.P("Projeto acadêmico e de portfólio — resultados sem validade clínica ou diagnóstica.", className="info"),
        html.P(
            [
                html.A(
                    [html.I(className="bi bi-github me-1"), "GitHub"],
                    href="https://github.com/sasaitals",
                    target="_blank",
                    rel="noopener noreferrer",
                    className="link-rodape"
                ),
                " | ",
                html.A(
                    [html.I(className="bi bi-linkedin me-1"), "LinkedIn"], 
                    href="https://www.linkedin.com/in/sabrinacostasantos/",
                    target="_blank",
                    rel="noopener noreferrer",
                    className="link-rodape"
                ),
            ]
        ),
    ],className='footer'
)

layout = html.Div([
    titulo,
    #vamos dividir a pagina em duas colunas com o .col mas para funcionar precisa estar dentro de um container
    formulario,
    load,
    html.Div(id='dummy-scroll'),
    rodape
], className='page')

@app.callback(
    Output('previsao', 'children'),
    [Input('botao-prever','n_clicks')],
    [State('idade','value'),
     State('sexo','value'),
     State('cp','value'),
     State('trestbps','value'),
     State('chol','value'),
     State('fbs','value'),
     State('restecg','value'),
     State('thalach','value'),
     State('exang','value'),
     State('oldpeak','value'),
     State('slope','value'),
     State('ca','value'),
     State('thal','value')]
)
def prever_doenca(n_clicks, idade, sexo, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    if n_clicks == 0:
        return ''
    
    time.sleep(2)

    
    entradas_usuario = pd.DataFrame(
        #            age	sex	cp	trestbps	chol	fbs	restecg	thalach	exang	oldpeak	slope	ca	thal
        data = [[idade, sexo, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
        columns = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    )

    #caso o usuario não possua todos os dados a serem fornecidos, o modelo usará a media deles
    entradas_usuario.fillna(medianas, inplace=True)

    #oldpeak é float 
    entradas_usuario['oldpeak'] = entradas_usuario['oldpeak'].astype(np.float64)

    #os outros dados 
    for col in entradas_usuario.columns:
        if col != 'oldpeak':
            entradas_usuario[col] = entradas_usuario[col].astype(np.int64)

    #converter numeros string->int
    for col in entradas_usuario.columns:
        entradas_usuario[col] = entradas_usuario[col].astype(int)

    #chamando o modelo para prever:
    previsao = modelo.predict(entradas_usuario)[0]
    #retorno do modelo:
    if previsao == 1:
        mensagem = "Você possui doença cardíaca!"
        cor_do_alerta = '#ff4031'
    else:
        mensagem = "Você não possui doença cardíaca!"
        cor_do_alerta = '#7de97f'

    alerta = dbc.Alert(mensagem, color=cor_do_alerta, className='resultado')
    return alerta

app.clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='scroll_bottom'),
    Output('dummy-scroll', 'children'),
    Input('botao-prever', 'n_clicks'),
    prevent_initial_call=True
)



