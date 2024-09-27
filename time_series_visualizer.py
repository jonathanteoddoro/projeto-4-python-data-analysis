# Importando as bibliotecas necessárias
import matplotlib.pyplot as plt
import pandas as pd  
import seaborn as sns  
from pandas.plotting import register_matplotlib_converters  
register_matplotlib_converters()  
import calendar  

# Carregando o conjunto de dados e configurando a coluna de data como índice
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Calculando os limites inferior e superior (2,5% e 97,5%) para remover outliers
inf = df['value'].quantile(0.025)
sup = df['value'].quantile(0.975)

# Filtrando o DataFrame para manter apenas os dados dentro dos limites
df = df[(df['value'] >= inf) & (df['value'] <= sup)].copy()

def draw_line_plot():
    # Função para desenhar um gráfico de linha
    
    plt.figure(figsize=(10, 5))  
    plt.plot(df.index, df['value'], color='r', linewidth=1)  # Desenha a linha com as páginas vistas ao longo do tempo
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')  
    plt.ylabel('Page Views')  
    
    fig = plt.gcf()  

    
    fig.savefig('line_plot.png')
    return fig  

def draw_bar_plot():
    # Função para desenhar um gráfico de barras
    
    df_bar = df.copy()  
    df_bar['year'] = df.index.year  
    df_bar['month'] = df.index.month  

    # Converte o número do mês para o nome do mês
    df_bar['month'] = df_bar['month'].apply(lambda x: calendar.month_name[x] if 1 <= x <= 12 else None)
    
    # Agrupa os dados por ano e mês, calculando a média das visualizações
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Mantém a ordem dos meses
    months_order = list(calendar.month_name[1:])
    df_grouped = df_grouped[months_order]  

    fig = plt.figure(figsize=(12, 8))  
    
    # Desenha o gráfico de barras
    df_grouped.plot(kind='bar', stacked=False, ax=plt.gca())

    # Rótulos e título do gráfico
    plt.xlabel('Years', fontweight='bold', fontsize=15)
    plt.ylabel('Average Page Views', fontweight='bold', fontsize=15)
    plt.title('Average Daily Page Views per Month (2016-2019)', fontweight='bold', fontsize=16)

    # Adiciona legenda
    plt.legend(title='Months', bbox_to_anchor=(1.05, 1), loc='upper left')

    
    fig.savefig('bar_plot.png')
    return fig  

def draw_box_plot():
    # Função para desenhar gráficos de caixa (box plots)
    
    df_box = df.copy()  
    df_box.reset_index(inplace=True)  
    df_box['year'] = [x.year for x in df_box.date]  
    df_box['month'] = [x.strftime('%b') for x in df_box.date]  

    # Define a ordem dos meses
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Cria uma figura com dois subgráficos
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    # Desenha o gráfico de caixa para visualizar a tendência ao longo dos anos
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)')  
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')  

    # Desenha o gráfico de caixa para visualizar a sazonalidade mensal
    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1], order=months)
    ax[1].set_title('Month-wise Box Plot (Seasonality)')  
    ax[1].set_xlabel('Month')  
    ax[1].set_ylabel('Page Views')  

    plt.tight_layout()  # Ajusta o layout para evitar sobreposição

    
    fig.savefig('box_plot.png')
    return fig  
