import pandas as pd
import plotly.express as px
from dash import dcc, html
import dash_bootstrap_components as dbc


# heart.csv é gerado uma única vez pelo gerar_dados.py
dados = pd.read_csv("heart.csv")

titulo = html.Div(
    html.H1("Analisando os dados!"),
    className='titulo'
)

figura_histograma = px.histogram(dados, x="age", title="Distribuição Etária - Histograma")
figura_histograma.update_xaxes(title_text='Idade')
figura_histograma.update_yaxes(title_text='')
div_do_histograma = html.Div([
            dcc.Graph(figure=figura_histograma),
            html.P(
                    [
                        "O gráfico mostra a quantidade de dados analisados distribuídos por idade. A maior concentração dos pacientes está entre 55 e 60 anos."
                    ], 
                    className="legenda-graficos"
            )
        ])


#adicionar cor no boxplot
dados_filtrados_boxplot = dados.copy()
dados_filtrados_boxplot['doenca'] = dados_filtrados_boxplot['doenca'].map({0: 'Não', 1: 'Sim'})
figura_boxplot = px.box(dados_filtrados_boxplot, x="doenca", y="age", color="doenca", title="Distribuição Etária - Boxplot")
figura_boxplot.update_xaxes(title_text='Quem possui doença')
figura_boxplot.update_yaxes(title_text='Idade')
figura_boxplot.update_layout(
    legend_title_text='Doença' # Altera o título da legenda para 'Gênero'
)
div_do_boxplot = html.Div([
        dcc.Graph(figure=figura_boxplot),
        html.P(
                [
                    "O gráfico mostra novamente a quantidade de dados analisados distribuídos por idade, porém separados por pacientes com e sem doença cardíaca. Pode-se constatar que 50% dos pacientes com a doença estão entre 52 e 62 anos."
                ], 
                className="legenda-graficos"
        )
    ])

#ViolinPlot
#Os pontos mostram cada uma das idades separadas por genero e apresentam apenas as pessoas que possuem doença
dados_filtrados_violin = dados[dados['doenca'] == 1].copy() #criando uma copia para não alterar o DataFrame original
dados_filtrados_violin['sex'] = dados_filtrados_violin['sex'].map({0: 'Feminino', 1: 'Masculino'}) #alterando o dados das colunas de 0 e 1 para feminino e masculino
dados_filtrados_violin['doenca'] = dados_filtrados_violin['doenca'].map({1: 'Dados analisados somente com pessoas positivas para a doença'})
cores_personalizadas = {'Masculino': 'blue', 'Feminino': 'red'} #Declarando cor para feminino e masculimo
figura_violin_chol = px.violin(dados_filtrados_violin, y="age", x="doenca", points='all', color="sex",
                title="Idade por Diagnósticos Positivos - Gênero - Violin",
                color_discrete_map=cores_personalizadas) # Aplica as cores personalizadas
figura_violin_chol.update_xaxes(title_text='')
figura_violin_chol.update_yaxes(title_text='Idade')
figura_violin_chol.update_layout(
    legend_title_text='Gênero' # Altera o título da legenda para 'Gênero'
)
div_do_violin_chol = html.Div([
            dcc.Graph(figure=figura_violin_chol),
            html.P(
                    [
                        "O gráfico mostra somente pacientes com diagnóstico positivo, por idade e gênero. Em ambos os gêneros, os casos se concentram entre 55 e 60 anos, e os homens aparecem com diagnóstico em idades mais precoces que as mulheres."
                    ], 
                    className="legenda-graficos"
            )
        ])


#PiePlot
#Usando somete dados de pesoas com doença
dados_filtrados_pie = dados[dados['doenca'] == 1].copy()
#nomeando os dados de restecg
dados_filtrados_pie['restecg'] = dados_filtrados_pie['restecg'].map({0: 'Normal',
                                                                    1: 'Anormalidade de onda ST-T',
                                                                    2: 'Hipertrofia ventricular esquerda'})
#Fazendo o frafico de pizza onde ele conta cada quantas pessoas com a doença tem cada resultado do eletro
figura_pie = px.pie(dados_filtrados_pie.groupby('restecg').size().reset_index(name='count'),
             values='count',
             names='restecg',
             title='Resultados do Eletrocardiograma em Repouso de Pessoas com Doença - Pie')
div_pie = html.Div([
    dcc.Graph(figure=figura_pie),
    html.P(
            [
                "O gráfico mostra, somente para pacientes com diagnóstico positivo, o resultado do eletrocardiograma em repouso. A maior parte apresenta hipertrofia ventricular esquerda."
            ], 
            className="legenda-graficos"
    )
])

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

#Abaixo vamos criar um html e colocaremos uma div com um grafico
layout = html.Div([
    titulo,
    dbc.Container([
        dbc.Row([
            dbc.Col([div_do_histograma], xs=12, lg=6, className='mb-4'),
            dbc.Col([div_do_boxplot], xs=12, lg=6, className='mb-4')
        ]),
        dbc.Row([
            dbc.Col([div_do_violin_chol], xs=12, lg=6, className='mb-4'),
            dbc.Col([div_pie], xs=12, lg=6, className='mb-4')
        ])
    ]),
    rodape
], className='page')