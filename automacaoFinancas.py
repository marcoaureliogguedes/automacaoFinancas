# Projeto de Automação

# Importando Bibliotecas
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
from cycler import cycler
from datetime import datetime, timedelta

yf.pdr_override()

# Analisando o índice IBOVESPA

# Digite em dias o período para ser analisado
dias = int(input('Digite o período em número de dias '))

data_inicial = datetime.now() - timedelta(days=dias)
data_final = datetime.now()

# Fazendo a requisição dos dados no yahoo finance
df_ibov = pdr.get_data_yahoo('^BVSP', data_inicial, data_final)['Adj Close']
df_ibov

# Calculando o retorno

# localizando o último e o primeiro preço
retorno = df_ibov.iloc[-1] / df_ibov.iloc[0] - 1
print('O retorno foi de: {:.2%}'.format(retorno))

# Gráfico
df_ibov.plot(label='IBOV', figsize=(15, 5), color='#091D40')

# Verificando a janela do tempo
media_movel = df_ibov.rolling(30).mean()

# Gráfico
media_movel.plot(label='MM30', color='#E28A7F')

# Exibindo a legenda
plt.legend()

# Exibindo o gráfico
plt.box(False)
plt.xticks(rotation=0)
plt.tick_params(axis='x', length=0)
plt.tick_params(axis='y', length=0)
plt.title('Análise do Índice IBOVESPA x Média Móvel', fontsize=15, fontweight='bold')
plt.ylabel('Preços em (R$)')
plt.show()

#=====================================#=============================================#

# Estilizando o gráfico

# Estilo
plt.style.use('dark_background')

# Gráfico
df_ibov.plot(label='IBOV', figsize=(15, 5))

# Verificando a janela do tempo
media_movel = df_ibov.rolling(30).mean()

# Gráfico
media_movel.plot(label='MM30')

# Exibindo a legenda
plt.legend()

# Exibindo o gráfico
plt.box(False)
plt.xticks(rotation=0)
plt.tick_params(axis='x', length=0)
plt.tick_params(axis='y', length=0)
plt.title('Análise do Índice IBOVESPA x Média Móvel', fontsize=15, fontweight='bold')
plt.ylabel('Preços em (R$)')
plt.show()

# PLOTLY
# Gráfico
fig = px.line(df_ibov, x=df_ibov.index, y='Adj Close',
              color_discrete_sequence=px.colors.qualitative.Set2,
              title='Análise do Índice IBOVESPA',
              template='plotly_dark')

fig.update_layout(xaxis=dict(rangeselector = dict(font = dict( color = "black"))))

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label='1m', step='month', stepmode='backward'),
            dict(count=6, label='6m', step='month', stepmode='backward'),
            dict(count=1, label='YTD', step='year', stepmode='todate'),
            dict(count=1, label='1y', step='year', stepmode='backward'),
            dict(step='all')
        ])
    )
)

fig.show()

# Cotação Máxima
cotacao_maxima = np.amax(df_ibov)
print(f'A cotação máxima do índice IBOVESPA no período foi de: {cotacao_maxima:,.0f}')

# Cotação Mínima
cotacao_minima = np.amin(df_ibov)
print(f'A cotação mínima do índice IBOVESPA no período foi de: {cotacao_minima:,.0f}')

# Cotação Atual
cotacao_atual = df_ibov.iloc[-1]
print(f'A cotação atual do índice IBOVESPA é de: {cotacao_atual:,.0f}')

# CARREGANDO OS DADOS DA CARTEIRA

df_carteira = pd.read_excel('carteira.xlsx')
df_carteira

dias = int(input('Digite o período em número de dias. '))

# Transformando a coluna de Ticker em uma lista python e Requisitando os dados dos ativos
data_inical = datetime.now() - timedelta(days=dias)
data_final = datetime.now()

# transformando a coluna Ticker em uma lista python
lista_ativos = list(df_carteira['Ticker'].astype(str) + '.SA')

# requisição
df_cotacoes = pdr.get_data_yahoo(lista_ativos, data_inical, data_final)['Adj Close']
df_cotacoes = round(df_cotacoes, 2)
df_cotacoes

# TRATAMENTO DE DADOS

# trazendo informações do dataframe
df_cotacoes.info()

# preencehdo valores vázios
df_cotacoes = df_cotacoes.ffill()

# NORMALIZANDO OS DADOS

# Criando um dataframe com os dados normalizados
df_cotacoesNorm = df_cotacoes / df_cotacoes.iloc[0]

# PLOTANDO UM GRÁFICO

# Estilo
plt.style.use('dark_background')

df_cotacoesNorm.plot(figsize=(15, 5))
plt.legend(loc='upper left')
plt.xticks(rotation=0)
plt.tick_params(axis='x', length=0)
plt.tick_params(axis='y', length=0)
plt.title('Carteira Normalizada', fontsize=15, fontweight='bold')
plt.box(False)
plt.show()

# Visualizando os ativos em gráficos individuais

# Estilo
plt.style.use('dark_background')

fig, axs = plt.subplots(nrows=9, ncols=1, figsize=(10,15), sharex=True)

ativos = ['AGRO3.SA', 'B3SA3.SA', 'EGIE3.SA', 'LEVE3.SA', 'ODPV3.SA', 'PRIO3.SA', 'PSSA3.SA', 'SUZB3.SA', 'WEGE3.SA']

for i, ativo in enumerate(ativos):
    axs[i].plot(df_cotacoesNorm.index, df_cotacoesNorm[ativo], label=ativo, color=f'C{i}')
    axs[i].legend()
    
fig.suptitle('Analisando a Variação Diária dos Ativos da Carteira', fontsize=12, fontweight='bold')
fig.supylabel('Variação Percentual')
    
plt.show()

# CALCULANDO O RETORNO DA CARTEIRA

# criando um dataframe vázio
df_valorInvestido = pd.DataFrame()

# percorrendo cada ativo do dataframe
for ativo in df_carteira['Ticker']:
    cotas = df_carteira.loc[df_carteira['Ticker'] == ativo, 'Cotas'].values[0]
    # criando uma nova coluna com os valores de cada ativo
    df_valorInvestido[ativo] = cotas * df_cotacoes[f'{ativo}.SA']
    
# criando uma nova coluna com o valor total
df_valorInvestido['Total'] = df_valorInvestido.sum(axis=1)   # somando todos os valores das colunas

df_valorInvestido = round(df_valorInvestido, 2)
df_valorInvestido

# COMPARANDO O RETORNO DA CARTEIRA COM O ÍNDICE IBOVESPA

# criando as duas tabelas normalizadas
df_ibovNorm = df_ibov / df_ibov.iloc[0]

# carteira normalizado
df_valorInvestidonorm = df_valorInvestido / df_valorInvestido.iloc[0]

df_ibovNorm.head()

# PLOTANDO UM GRÁFICO DO HISTÓRICO

# Estilo
plt.style.use('dark_background')

df_valorInvestidonorm['Total'].plot(figsize=(15, 5), label='Carteira')
df_ibovNorm.plot(label='IBOV')

plt.legend()
plt.xticks(rotation=0)
plt.tick_params(axis='x', length=0)
plt.tick_params(axis='y', length=0)
plt.title('Retorno da Carteira vs IBOVESPA', fontsize=15, fontweight='bold')
plt.box(False)

plt.show()

# CALCULANDO O RETORNO E A CORRELAÇAO

# retorno IBOVESPA
retorno_ibov = df_ibovNorm[-1] -1 # o cálculo aqui foi feito direto porque a dataframe já está normalizado

# retorno da Carteira
retorno_carteira = df_valorInvestidonorm['Total'][-1] -1 

# imprimindo o retorno
print(f'O retorno do IBOV foi de: {retorno_ibov:.2%}')
print(f'O retorno da Carteira de Investimentos foi de: {retorno_carteira:.2%}')

# correlação
correlacao = df_valorInvestido['Total'].corr(df_ibov)

print(f'A correlação da Carteira de Investimentos e o IBOV foi de: {correlacao:.2%}')