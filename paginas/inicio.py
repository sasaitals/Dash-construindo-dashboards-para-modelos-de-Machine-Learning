from dash import html
import dash_bootstrap_components as dbc
import joblib


titulo = html.Div(
    html.H1("Apresentação"),
    className='titulo'
)

apresentacao_paginas = dbc.Container([
    html.P(
        [
            "Seja bem-vindo! Este projeto foi desenvolvido como parte do meu portfólio, durante o curso Dash: Construindo Dashboards para Modelos de Machine Learning, oferecido pela Alura. Ao longo do curso, foi utilizado o dataset Heart Disease, disponibilizado no UCI Machine Learning Repository, um repositório de conjuntos de dados criado em 1987 por David Aha, então doutorando na Universidade da Califórnia, Irvine (UCI). A plataforma é amplamente utilizada por estudantes, pesquisadores e profissionais para o desenvolvimento e a avaliação de algoritmos de Machine Learning.",
            html.Br()
        ]),
    dbc.Row([
        dbc.Col([
            html.H4("Página Dashboard:"),
            html.P([
                "Um dashboard é um painel visual que organiza informações de forma estruturada, facilitando a interpretação dos dados e a identificação de padrões relevantes. A página Dashboard apresenta visualizações gráficas utilizadas na análise exploratória dos dados que fundamentam o desenvolvimento do modelo de Machine Learning, apresentado na página seguinte. "
            ])
        ], xs=12, lg=6, className='mb-4'),
        dbc.Col([
            html.H4("Página Formulário:"),
            html.P([
                "A página Formulário apresenta um questionário que utiliza dados clínicos e resultados de exames do paciente para indicar se há ou não indícios de doença cardíaca por meio de um modelo de Machine Learning desenvolvido durante o curso. O Machine Learning é um ramo da Inteligência Artificial (IA) que permite aos sistemas identificar padrões a partir de dados e realizar previsões. Enquanto a IA constitui um campo mais amplo, que abrange diferentes técnicas para a execução de tarefas que normalmente exigiriam inteligência humana, o Machine Learning é uma das suas abordagens, permitindo que os modelos aprendam padrões a partir de dados utilizados no treinamento e apliquem esse conhecimento a novas informações para gerar previsões."
            ])
        ], xs=12, lg=6, className='mb-4')
    ])
], className='inicio')

metricas = joblib.load('metricas.pkl')
acuracia = metricas['acuracia']

sobre_acuracia = dbc.Container([
    html.H2(f"A acurácia do modelo é de {acuracia: .1%}"),
    html.H4("O que é acurácia?"),
    html.P([
            f"Acurácia nada mais é do que a porcentagem de previsões corretas do modelo com os dados de teste, ou seja, o modelo possui {acuracia:.1%} de previsões corretas nos dados de teste, por isso este sistema não é 100% exato!"
        ])
], className='inicio')

sobre_mim = dbc.Container([
    html.H4("Sobre mim"),
    dbc.Row([
        dbc.Col([
            html.Img(
                src="/assets/profile.jpg",
                alt="Foto de Sabrina",
                className='img'
            )
        ], xs=12, lg="auto", className='mb-3'),
        dbc.Col([
            html.P([
                "Olá! Sou Sabrina, formada em Análise e Desenvolvimento de Sistemas, e atualmente estou aprofundando meus conhecimentos em Ciência de Dados e Machine Learning.",
                html.Br(),
                html.Br(),
                "Desde meados de 2026, venho desenvolvendo projetos práticos e aprimorando minhas habilidades, principalmente por meio dos cursos da Alura. Este é o primeiro de muitos projetos que pretendo desenvolver para consolidar meus conhecimentos e explorar novas possibilidades nessa área.",
                html.Br(),
                html.Br(),
                "Fique à vontade para conhecer meus outros projetos no GitHub e no LinkedIn, disponíveis no rodapé!"
            ], className='texto-sobre')
        ], xs=12, lg=7, className='mb-3')
    ], align="center", justify="center", className="g-4")
], className='inicio')


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
    apresentacao_paginas,
    sobre_acuracia,
    sobre_mim,
    rodape
], className='page')
