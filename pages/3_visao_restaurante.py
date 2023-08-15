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

st.set_page_config(page_title = 'Visão Restaurantes', page_icon = 'pages/restaurante_2.png', layout = 'wide')

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
# Calcula a distância
# =================================================

def distance(df_1, fig):
        ''' Esta função calcula a distância média por cidade e por tipo de pedidos
            Parâmetros:
                Input:
                    - df_1: Dataframe com os dados necessário para cáculo
                Output:
                    - df_1: Dataframe com 4 colunas e 12 linha
                    - fig: Gráfico de Pizza (Pie)
        
        '''
        if fig == False:
            colunas = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            df_1['Distance_km'] = df_1.loc[ : ,colunas].apply(lambda x: hs((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)
        
            media_distance = np.round(df_1['Distance_km'].mean(), 2)
            
            return media_distance
            
        else:
            colunas = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            df_1['Distance_km'] = df_1.loc[ : ,colunas].apply(lambda x: hs((x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)

            media_distance = df_1.loc[ : , ['City', 'Distance_km']].groupby('City').mean().reset_index()
                        
            # Exibir na tela
            fig = go.Figure(data = [go.Pie(labels = media_distance['City'], values = media_distance['Distance_km'], pull = [0, 0.1, 0])])
            
            return fig

# ======================================================
# Calcula o tempo e o desvio padrão do tempo de entrega
# ======================================================    

def media_std_time_delivery(df_1, festival, op):
    ''' Esta função calcula o tempo e o desvio padrão do tempo de entrega
        Parâmetros:
            Input:
                - df_1: Dataframe com os dados necessário para cáculo
                - op: Tipo de operação que precisa ser calculado
                    'Media_time': Calcula o tempo médio
                    'Desvio_padrao_time': Calcula o desvio padrão do tempo
            Output:
                - df_1: Dataframe com 2 colunas e 1 linha
    
    '''
    # Calculando o tempo médio e desvio padrão
    df_1_aux = df_1.loc[ : , ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)' : ['mean', 'std']})
    
    # Mudando nome de colunas
    df_1_aux.columns = ['Media_time', 'Desvio_padrao_time']
    
    # Resetando o ndex
    df_1_aux = df_1_aux.reset_index()
    
    # Atribuindo somente o valor 'Yes' nas linhas
    df_1_aux = np.round(df_1_aux.loc[df_1_aux['Festival'] == festival, op], 2)

    return df_1_aux

# ======================================================
# Calcula o gráfico de barras (bar)
# ======================================================

def media_std_time_graph(df_1):
    ''' Esta função calcula o gráfico de barras (bar)
        Parâmetros:
            Input:
                - df_1: Dataframe com os dados necessário para cáculo
            Output:
                - fig: Gráfico de barras (bar)
    
    '''
    # Criando duas colunas: média e desvio padrão do tempo de entrega por cidade
    df_1_aux = df_1.loc[ : , ].groupby('City')['Time_taken(min)'].agg(['mean', 'std']).reset_index()
        
    # Renomeando as colunas
    df_1_aux.columns = ['City', 'Media_time', 'Desvio_padrao_time']
        
    # Criando o gráfico de barras
    fig = go.Figure()
        
    # Adicionando a barra de média com desvio padrão como erro
    fig.add_trace(go.Bar(name = 'Control', x = df_1_aux['City'], y = df_1_aux['Media_time'], error_y = dict(type ='data', array = df_1_aux['Desvio_padrao_time']), ))
        
    # Configurando o modo de exibição das barras (grupo, ao invés de sobrepostas)
    fig.update_layout(barmode = 'group')

    return fig

# ======================================================
# Calcula o gráfico de sol (sunburst)
# ======================================================

def media_std_time_on_traffic(df_1):
    ''' Esta função calcula o gráfico de sol (sunburst)
        Parâmetros:
            Input:
                - df_1: Dataframe com os dados necessário para cáculo                
            Output:
                - fig: Gráfico de sol (sunburst)
    
    '''
    # Agrupando por cidade e densidade de tráfego e calculando média e desvio padrão do tempo de entrega
    df_1_aux = df_1.groupby(['City', 'Road_traffic_density'])['Time_taken(min)'].agg(['mean', 'std']).reset_index()
    
    # Renomeando as colunas
    df_1_aux.columns = ['City', 'Road_traffic_density', 'Media_time', 'Desvio_padrao_time']
    
    # Criando o gráfico de sunburst
    fig = px.sunburst(df_1_aux, path = ['City', 'Road_traffic_density'], values = 'Media_time', color = 'Desvio_padrao_time', 
                      color_continuous_scale = 'Bluered')

    return fig
    
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

st.header('Marketplace - Visão Restaurantes')

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
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '_', '_'])

with tab1:
    
    # Container do topo Visão Gerencial
    with st.container():
    
        # Título Order Matric
        st.markdown('### Overall Metrics')
        col1, col2, col3, col4, col5, col6 = st.columns(6, gap = 'large')
        
        with col1:

            # Contagem de entregadores únicos
            entregadores_unicos = len(df_1.loc[ : ,'Delivery_person_ID'].unique())

            col1.metric('Entregadores', entregadores_unicos)

        with col2:
            media_distance = distance(df_1, fig = False)
            # Exibir na tela
            col2.metric('Distância média', media_distance)

        with col3:
            df_1_aux = media_std_time_delivery(df_1, 'Yes', 'Media_time')
            # Exibir na tela
            col3.metric('Tempo Médio', df_1_aux)

        with col4:
            df_1_aux = media_std_time_delivery(df_1, 'Yes', 'Desvio_padrao_time')
            # Exibir na tela
            col4.metric('STD Médio', df_1_aux)                    
 
        with col5:
            df_1_aux = media_std_time_delivery(df_1, 'No', 'Media_time')
            # Exibir na tela
            col5.metric('Tempo Médio', df_1_aux)
             
        with col6:
            df_1_aux = media_std_time_delivery(df_1, 'No', 'Desvio_padrao_time')
            # Exibir na tela
            col6.metric('STD Médio', df_1_aux)                      

    # Container do topo Visão Gerencial
    with st.container():
        
        st.markdown('''___''')
        
        # Título Order Matric
        st.markdown('### Tempo de entrega por cidade')

        col1, col2 = st.columns(2, gap = 'large')

        with col1:
            fig = media_std_time_graph(df_1)
            # Exibindo o gráfico no Streamlit
            st.plotly_chart(fig)
        
        with col2:
        
            st.markdown('''___''')
                    
            # Criando colunas vazia
            colunas = ['City', 'Time_taken(min)', 'Type_of_order']
            
            # Calculando o tempo médio e desvio padrão
            df_1_aux = df_1.loc[ : , colunas].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)' : ['mean', 'std']})
            
            # Mudando nome de colunas
            df_1_aux.columns = ['Media_time', 'Desvio_padrao_time']
            
            # Resetando o ndex
            df_1_aux = df_1_aux.reset_index()
            
            # Exibir na tela
            st.dataframe(df_1_aux)
        
    # Container do topo Visão Gerencial
    with st.container():
        
        st.markdown('''___''')
                
        # Título Order Matric
        st.markdown('### Distribuição do tempo')
        
        col1, col2 = st.columns(2, gap = 'large')
        
        with col1:
            fig = distance(df_1, fig = True)
            # Exibindo o gráfico no Streamlit
            st.plotly_chart(fig)

        with col2:
            fig = media_std_time_on_traffic(df_1)
            # Exibindo o gráfico no Streamlit
            st.plotly_chart(fig)
            
            
        
