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

st.set_page_config(page_title = 'Visão Entregador', page_icon = 'pages/entregador.png', layout = 'wide')

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
    
    # Converter a coluna de object para float
    df_1['Delivery_person_Ratings'] = df_1['Delivery_person_Ratings'].astype(float)
    
    # convertendo a coluna 'Order_Date' de texto para Data
    df_1['Order_Date'] = pd.to_datetime(df_1['Order_Date'], format = '%d-%m-%Y')
    
    # Forma 3: Removendo os espaços dentro de strings/texto/object trocando nome das colunas
    df_1['Time_taken(min)'] = df_1['Time_taken(min)'].apply(lambda x: x.split('(min) ')[1]).astype(int)

    return df_1

# ===========================================================================
# Funções Calculando os entregadores mais rápido e os mais lento por cidade
# ===========================================================================

def top_delivers(df_1, top_asc):

    ''' Esta função tem a responsabilidade de Calculando os entregadores mais rápido e os mais lento por cidade
    
    Tipos de limpeza:
    1. Calculando os entregadores mais rápido
    2. Calculando os entregadores mais lento

    Input: DataFrame, top_asc
    Output: DataFrame
    '''
    
    # Calculando o entregadores mais rápido e o mais lento por cidade
    df_2 = df_1.loc[ : , ['City', 'Delivery_person_ID', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).mean().sort_values(['City', 'Time_taken(min)'], ascending = top_asc).reset_index()
        
    # Contagem dos 10  entregadores  mais rápido e o mais lento por cidade
    entregadores_lento_cidade1 = df_2.loc[df_2['City'] == 'Metropolitian', : ].head(10)
    entregadores_lento_cidade2 = df_2.loc[df_2['City'] == 'Urban', : ].head(10)
    entregadores_lento_cidade3 = df_2.loc[df_2['City'] == 'Semi-Urban', : ].head(10)
        
    # Juntando as variavel
    df_1_aux = pd.concat([entregadores_lento_cidade1, entregadores_lento_cidade2, entregadores_lento_cidade3]).reset_index(drop = True)

    return df_1_aux

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

st.markdown('# Marketplace - Visão Entregadores')

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
tab1, tab2, tab3 = st.tabs(['Overall Metrics', '_', '_'])

with tab1:
    
    # Container do topo Visão Gerencial
    with st.container():
    
        # Título Order Matric
        st.markdown('### Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap = 'large')
        
        with col1:
            
            # A maior idade dos entregadores
            maior_idade_entregadores = df_1.loc[ : , 'Delivery_person_Age'].max()

            col1.metric('Maior de idade', maior_idade_entregadores)

        with col2:
                       
            # A menor idade dos entregadores
            menor_idade_entregadores = df_1.loc[ : , 'Delivery_person_Age'].min()
            
            col2.metric('Menor de idade', menor_idade_entregadores)

        with col3:
                        
            # A melhor condição de veículos
            melhor_condição_veiculos = df_1.loc[ : , 'Vehicle_condition'].max()
            
            col3.metric('Melhor condição de veículo', melhor_condição_veiculos)

        with col4:
                      
            # A pior condição de veículos
            pior_condição_veiculos = df_1.loc[ : , 'Vehicle_condition'].min()
            
            col4.metric('Pior condição de veículo', pior_condição_veiculos) 
     
    
    # Container do meio Avaliações
    with st.container():
        
        st.markdown('''___''')
        
        # Título Avaliações
        st.markdown('### Avaliações')
        col1, col2 = st.columns(2, gap = 'large')
            
        with col1:
    
            st.markdown('###### Avaliação média por entregador')
                
            # Caulcular a avaliação média por entregador
            media_avaliacao_entregadores = (df_1.loc[ : ,['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index())
    
            # Exibir na tela
            st.dataframe(media_avaliacao_entregadores)
    
        with col2:
            st.markdown('###### Avaliação média por trânsito')
                
            # Calcular a avaliação média por tipo de tráfego
            media_desvio_avaliacao_trafego = (df_1.loc[ : , ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings' : ['mean', 'std']}))
    
            # Mudando o nome das colunas que estão com mult index
            media_desvio_avaliacao_trafego.columns = ['Mean_ratings', 'Std_ratings']
                
            # Exibir na tela
            st.dataframe(media_desvio_avaliacao_trafego.reset_index())
                
            st.markdown('###### Avaliação média por clíma')
            # Calcular a avaliação média por tipo de tráfego
            media_desvio_avaliacao_climaticas = (df_1.loc[ : , ['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions')
                                                      .agg({'Delivery_person_Ratings' : ['mean', 'std']}))
    
            # Mudando o nome das colunas que estão com mult index
            media_desvio_avaliacao_climaticas.columns = ['Mean_ratings', 'Std_ratings']
                
            # Exibir na tela
            st.dataframe(media_desvio_avaliacao_climaticas.reset_index())

    
    # Container do fundo Velocidade de entrega
    with st.container():

        st.markdown('''___''')
        
        # Título Velocidade de entrega
        st.markdown('### Velocidade de entrega')
        col1, col2 = st.columns(2, gap = 'large')
            
        with col1:
            st.markdown('###### Top entregadores mais rápidos')
            df_1_aux = top_delivers(df_1, top_asc = True)
            # Exibir na tela
            st.dataframe(df_1_aux)
    
        with col2:
            st.markdown('###### Top entregadores mais lentos')
            df_1_aux = top_delivers(df_1, top_asc = False)
            # Exibir na tela
            st.dataframe(df_1_aux)
