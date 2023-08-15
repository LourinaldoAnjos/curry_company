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
import streamlit as st
from PIL import Image

# ========================================================================= Configuração da pagina =========================================================================

st.set_page_config(page_title = 'pages/Home', page_icon = 'pages/dashboard_5.png')

# ==========================================================================================================================================================================

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

st.write('# Curry Company Growth Dashboard')

st.markdown(
    '''
    Growth Dashboard foi construido para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanias de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
    ### Ask for Help
    - Time de Data Science no Discord
        - @lourinaldo
    ''' )
