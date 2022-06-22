from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")

# criando o gráfico
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

# Pegando todos os valores unicos da coluna
# "ID Loja" e criando um lista Python das Lojas
lojas = list(df['ID Loja'].unique())
# Adicionando a lista um novo item
lojas.append("Todas as Lojas")

# Criando o Layout da página com html e dcc
app.layout = html.Div(children=[
    html.H1(children='Faturamento das Lojas'),
    html.H2(children='Gráfico com o Faturamento de Todos os Produtos separados por Loja'),
    html.Div(children='''
        Obs: Esse gráfico mostra a quantidade de produtos vendidos, não o faturamento.
    '''),
    # Carregando Dropdown passando a varivel lojas, value
    # com o valor adicionado na lista e o id que é nome do Dropdown
    dcc.Dropdown(lojas, value='Todas as Lojas', id='lista_lojas'),
    # Carregando grafico
    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
    )
])

# callback para modificar as as informações da página de forma dinâmica
# ele sempre vai ter um Input e Output
@app.callback(
    # Output é quem sera modificado
    Output('grafico_quantidade_vendas', 'figure'),
    # Input é quem seleciona o valor
    Input('lista_lojas', 'value')
)
def update_output(value):
    if value == "Todas as Lojas":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[value == df['ID Loja'], :]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)