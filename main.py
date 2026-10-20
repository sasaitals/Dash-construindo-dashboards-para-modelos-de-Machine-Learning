from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import paginas
from app import app


navegacao = navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Dashboard', href='/graficos', active='exact')),
        dbc.NavItem(dbc.NavLink('Formulário', href='/formulario', active='exact'))
    ],
    brand="Início",
    brand_href="/",
    color="primary",
    dark=True,
    className="navegacao"
)

app.layout = html.Div([
    navegacao,
    dcc.Location(id='url', refresh=False),
    html.Div(id='conteudo')
])


@app.callback(
    Output('conteudo','children'),
    [Input('url','pathname')]
)

def mostrar_pagina(pathname):
    if pathname == '/formulario':
        return paginas.formulario.layout
    elif pathname == '/graficos':
        return paginas.graficos.layout
    else:
        return paginas.inicio.layout



app.run(debug=False)