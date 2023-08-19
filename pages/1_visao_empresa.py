# Libraries
from haversine import haversine as hs
from datetime import datetime
from streamlit_folium import folium_static

# Bibliotecas necessárias
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import folium as fl

# ========================================================================= Configuração da pagina =========================================================================

st.set_page_config(page_title = 'Visão Empresa', page_icon = 'pages/empresa.png', layout = 'wide')

# ================================================================================ Funções ================================================================================

# =================================================
# Limpeza do dataframe
# =================================================

def clean_code(df_1):

    ''' Esta função tem a responsabilidade de limpar o dataframe
    
    Tipos de limpeza:
    1. Remoção dos dados NaN
    2. Mudança do tipo da coluna de dados
    3. Remoção dos espaços das variável de texto
    4. Formatação da coluna de datas
    5. Limpeza da coluna de tempo (remoção do texto da variável numérica)

    Input: DataFrame
    Output: DataFrame    
    '''
    # Removendo os espaços dentro de strings/texto/object trocando nome das colunas
    df_1.loc[ : , 'Delivery_person_Age'] = df_1.loc[ : , 'Delivery_person_Age'].str.strip()
    df_1.loc[ : , 'Road_traffic_density'] = df_1.loc[ : , 'Road_traffic_density'].str.strip()
    df_1.loc[ : , 'City'] = df_1.loc[ : , 'City'].str.strip()
    df_1.loc[ : , 'Festival'] = df_1.loc[ : , 'Festival'].str.strip()
    
    # Limpando os NaN das colunas
    linhas_selecionadas = (df_1['Delivery_person_Age'] != 'NaN')
    
    # Copia das colunas com as linhas_selecionadas limpas dos NaN
    df_1 = df_1.loc[linhas_selecionadas, : ].copy()
    
    # Converter a coluna de object para int
    df_1['Delivery_person_Age'] = df_1['Delivery_person_Age'].astype(int)
    
    # Limpando os NaN das colunas
    linhas_selecionadas = (df_1['Road_traffic_density'] != 'NaN')
    
    # Copia das colunas com as linhas_selecionadas limpas dos NaN
    df_1 = df_1.loc[linhas_selecionadas, : ].copy()
    
    # Limpando os NaN das colunas
    linhas_selecionadas = (df_1['City'] != 'NaN')
    
    # Copia das colunas com as linhas_selecionadas limpas dos NaN
    df_1 = df_1.loc[linhas_selecionadas, : ].copy()
    
    # Limpando os NaN das colunas
    linhas_selecionadas = (df_1['Festival'] != 'NaN')
    
    # Copia das colunas com as linhas_selecionadas limpas dos NaN
    df_1 = df_1.loc[linhas_selecionadas, : ].copy()
    
    # Converter a coluna de object para float
    df_1['Delivery_person_Ratings'] = df_1['Delivery_person_Ratings'].astype(float)
    
    # convertendo a coluna 'Order_Date' de texto para Data
    df_1['Order_Date'] = pd.to_datetime(df_1['Order_Date'], format = '%d-%m-%Y')
    
    # Forma 3: Removendo os espaços dentro de strings/texto/object trocando nome das colunas
    df_1['Time_taken(min)'] = df_1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1]).astype(int)

    return df_1
    
# =================================================
# Funções Desenhar o gráfico de barras (bar) Plotly
# =================================================

def order_metric(df_1):

    ''' Esta função tem a responsabilidade de Desenhar o gráfico de barras (bar)Plotly
    
    Tipos de gráfico:
    1. Gráfico de barras

    Input: DataFrame
    Output: fig    
    '''

    # Cria colunas vazias 'ID' e 'Order_Date'
    colunas_vazias = ['ID', 'Order_Date']

    # Contagem das colunas 'ID' e 'Order_Date'
    df_1_aux = df_1.loc[ : , colunas_vazias].groupby('Order_Date').count().reset_index()
    
    # Desenhar o gráfico de barras Plotly
    fig = px.bar(df_1_aux, x = 'Order_Date', y = 'ID')

    return fig

# =================================================
# Funções Desenhar o gráfico de pizza (pie) Plotly
# =================================================

def traffic_order_share(df_1):

    ''' Esta função tem a responsabilidade de Desenhar o gráfico de pizza (pie) Plotly
    
    Tipos de gráfico:
    1. Gráfico de pizza

    Input: DataFrame
    Output: fig    
    '''

    # Contagem das colunas 'ID' e 'Road_traffic_density'
    df_1_aux = df_1.loc[ : ,['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()

    # Criar coluna vazia 'Entregas_porcentual'
    resutado_porc = df_1_aux['Entregas_porcentual'] = df_1_aux['ID'] / df_1_aux['ID'].sum()

    # Desenhar o gráfico de pizza (pie) Plotly
    fig = px.pie(df_1_aux, values = 'Entregas_porcentual', names = 'Road_traffic_density')

    return fig

# =================================================
# Funções Desenha gráfico de bolhas (scatter)
# =================================================

def Traffic_order_city(df_1):

    ''' Esta função tem a responsabilidade de Desenhar o gráfico de bolhas (scatter)
    
    Tipos de gráfico:
    1. Gráfico de bolhas

    Input: DataFrame
    Output: fig    
    '''
    
    # Contagem do agrupamento com 'ID', 'City' e 'Type_of_vehicle'
    df_1_aux = df_1.loc[ :, ['ID', 'City', 'Type_of_vehicle']].groupby(['City', 'Type_of_vehicle']).count().reset_index()

    # Desenha gráfico de bolhas (scatter)
    fig = px.scatter(df_1_aux, x = 'City', y = 'Type_of_vehicle', size = 'ID', color = 'City')

    return fig

# =================================================
# Funções Desenhar gráfico de linhas (line) Plotly
# =================================================

def order_by_week(df_1):

    ''' Esta função tem a responsabilidade de Desenhar o gráfico de linhas (line) Plotly
    
    Tipos de gráfico:
    1. Gráfico de linhas

    Input: DataFrame
    Output: fig    
    '''

    # Criar coluna vazia de semana
    df_1['Week_year'] = df_1['Order_Date'].dt.strftime('%U')
    
    # Contagem das colunas'ID', 'Week_year'
    df_1_aux = df_1.loc[ : , ['ID', 'Week_year']].groupby('Week_year').count().reset_index()
    
    # Desenhar gráfico de linhas (line) Plotly
    fig = px.line(df_1_aux, x = 'Week_year', y = 'ID')

    return fig 

# =================================================
# Funções Desenhar gráfico de linhas (line) Plotly
# =================================================

def order_share_by_week(df_1):

    ''' Esta função tem a responsabilidade de Desenhar o gráfico de linhas (line) Plotly
    
    Tipos de gráfico:
    1. Gráfico de linhas

    Input: DataFrame
    Output: fig    
    '''

    # Contagem coluna 'ID' e 'Week_of_year'
    df_1_aux = df_1.loc[ :, ['ID', 'Week_year']].groupby('Week_year').count().reset_index()
            
    # Contagem única dos entregadores
    df_2_aux = df_1.loc[ :, ['Delivery_person_ID','Week_year']].groupby('Week_year').nunique().reset_index()
            
    # Juntar 2 DataFrame
    df_aux = pd.merge(df_1_aux, df_2_aux, how = 'inner')
            
    # Divisão entre o número total de pedidos na semana e a quantidade de entregadores únicos naquela mesma semana.
    df_aux['Order_by_deliver'] = df_1_aux['ID'] / df_2_aux['Delivery_person_ID']
            
    # Desenhar gráfico de linha (line)
    fig = px.line(df_aux, x = 'Week_year', y = 'Order_by_deliver')

    return fig

# =================================================
# Funções Desenha o mapa do mundo com pino
# =================================================

def country_maps(df_1):

    ''' Esta função tem a responsabilidade de Desenhar o mapa do mundo com pino
    
    Tipos de gráfico:
    1. Mapa do mundo com pino

    Input: DataFrame
    Output: None    
    '''
    
    # Calcular o valor mediano da latitude e da longitude agrupar por cidade e tipo de tráfego
    df_1_aux = df_1.loc[ :, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City','Road_traffic_density']).median().reset_index()
    
    # Desenha o mapa do mundo
    map = fl.Map()
    
    # Preencher o mapa com as informações solicitadas
    for index, location_info in df_1_aux.iterrows():
      fl.Marker([location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']], popup = location_info[['City', 'Road_traffic_density']]).add_to(map)

    # Desenha o mapa do mundo com pino
    folium_static(map, width = 800, height = 500)
    
    return None
    
# ================================================================= Inicio da Estrutura lógica do código =================================================================

# =================================================
# Import  dataframe
# =================================================
df = pd.read_csv('dataset/train.csv')

# =================================================
# Copiando o DataFrame original
# =================================================
df_1 = df.copy()

# =================================================
# Limpando os daos
# =================================================
df_1 = clean_code(df_1)

# =================================================
# Barra Lateral - Streamlit
# =================================================

st.header('Marketplace - Visão Entregadores')

image_path = 'pages/logo.png'

image = Image.open(image_path)

st.sidebar.image(image, width = 150)

st.sidebar.markdown('# Cury Company')

st.sidebar.markdown('## Fastest Delivery in Town')

st.sidebar.markdown('''____''')

st.sidebar.markdown('## Selecione uma data limite')

# Definir os valores mínimos e máximos
min_date = datetime(2022, 2, 11)
max_date = datetime(2022, 4, 6)

# Usar um slider para selecionar a data
date_slider = st.sidebar.slider(
    'Até qual Data?',
    value = datetime(2022, 4, 14),
    min_value = min_date,
    max_value = max_date,
    format = 'DD-MM-YYYY')

# Divisa da Seleção de data limite
st.sidebar.markdown('''____''')

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam'])

# Divisa da Seleção de data limite
st.sidebar.markdown('''____''')

Weather_options = st.sidebar.multiselect(
    'Quais as condições do clíma',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default = ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'] )

# Divisa da Seleção de data limite
st.sidebar.markdown('''____''')

city_options = st.sidebar.multiselect(
    'Quais as cidade',
    ['Metropolitian', 'Urban', 'Semi-Urban'],
    default = ['Metropolitian', 'Urban', 'Semi-Urban'])

# Divisa da Seleção de Quais as condições do trânsito
st.sidebar.markdown('''___''')

# Divisa dos créditos do autor
st.sidebar.markdown('### Power by Comunidade DS')

# Filtro por data
linhas_selecionadas = df_1['Order_Date'] < date_slider
df_1 = df_1.loc[linhas_selecionadas, : ]

# Filtro por trânsito
linhas_selecionadas = df_1['Road_traffic_density'].isin(traffic_options)
df_1 = df_1.loc[linhas_selecionadas, : ]

# Filtro por clíma
linhas_selecionadas = df_1['Weatherconditions'].isin(Weather_options)
df_1 = df_1.loc[linhas_selecionadas, : ]

# Filtro por cidade
linhas_selecionadas = df_1['City'].isin(city_options)
df_1 = df_1.loc[linhas_selecionadas, : ]

# ==================================================================== Inicio do Layout no Streamlit ====================================================================

# =================================================
# Menu de navegação no Layout no Streamlit
# =================================================

# Menu de navegação no Layout no Streamlit
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geografica'])

with tab1:
    
    # Container do topo Visão Gerencial
    with st.container():
        fig = order_metric(df_1)
        # Título Order Matric
        st.markdown('### Orders by Day')
        # Plotar na tela
        st.plotly_chart(fig, use_container_witdth = True)
        
    # Container do meio colunas 1
    with st.container():
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            fig = traffic_order_share(df_1)
            # Título da coluna 1
            st.markdown('### Traffic Order Share')
            # Plotar na tela
            st.plotly_chart(fig, use_container_witdth = True)

    # Container do meio colunas 2
    with st.container(): 
        
        with col2:
            fig = Traffic_order_city(df_1)
            # Título da coluna 2
            st.markdown('### Traffic Order City')
            # Plotar na tela
            st.plotly_chart(fig, use_container_witdth = True)
       
with tab2:
    
    # Container do meio 1 Visão Tática
    with st.container():
        fig = order_by_week(df_1)
        # Título 1 do meio
        st.markdown('### Order by Week')
        # Plotar na tela
        st.plotly_chart(fig, use_container_witdth = True)

    # Container do meio 2 Visão Tática
    with st.container():
        fig = order_share_by_week(df_1)
        # Título 2 do meio
        st.markdown('### Order Share by Week')         
        # Plotar na tela
        st.plotly_chart(fig, use_container_witdth = True)

with tab3:
    
    # Container do fundo Visão Geografica
    with st.container():
        # Título Fundo
        st.markdown('### Country Maps')
        fig = country_maps(df_1)
                   

