import streamlit as st
import logging
import os
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="📊 Painel de Arquivos Processados", layout="wide", initial_sidebar_state="expanded")

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho relativo onde estão os arquivos processados
PASTA_PROCESSADOS = "data/arquivos_processados"

# Verifica se a pasta existe, caso contrário, cria a pasta
if not os.path.exists(PASTA_PROCESSADOS):
    logging.warning(f"A pasta {PASTA_PROCESSADOS} não foi encontrada. Criando a pasta...")
    os.makedirs(PASTA_PROCESSADOS, exist_ok=True)

def listar_arquivos():
    """Lista os arquivos CSV na pasta de processados (sem subpastas)"""
    if not os.path.exists(PASTA_PROCESSADOS):
        logging.error(f"A pasta {PASTA_PROCESSADOS} não foi encontrada!")
        return []
    return [f for f in os.listdir(PASTA_PROCESSADOS) if f.lower().endswith(".csv")]

def carregar_dados(arquivo):
    """Carrega um arquivo CSV em um DataFrame"""
    caminho_arquivo = os.path.join(PASTA_PROCESSADOS, arquivo)
    logging.info(f"Tentando carregar o arquivo: {caminho_arquivo}")
    try:
        return pd.read_csv(caminho_arquivo, sep=";", encoding="latin-1")
    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo {arquivo}: {e}")
        return None

# Interface do Streamlit
st.markdown("""
    <style>
        .css-1d391kg {background-color: #1E1E1E;}
        .stApp {background-color: #0E0E0E; color: white;}
        .stTextInput, .stSelectbox, .stDataFrame, .stPlotlyChart {background-color: #222222; color: white; border-radius: 10px; padding: 10px;}
        .stButton button {background-color: #4CAF50; color: white; font-size: 16px;}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Painel de Arquivos Processados")
st.sidebar.header("🔍 Opções de Filtro")

# Lista os arquivos disponíveis
arquivos = listar_arquivos()
if arquivos:
    arquivo_selecionado = st.sidebar.selectbox("Selecione um arquivo para visualizar:", arquivos)
    df = carregar_dados(arquivo_selecionado)
    if df is not None:
        st.subheader(f"📂 Visualizando: {arquivo_selecionado}")
        st.dataframe(df.style.set_properties(**{'background-color': '#2E2E2E', 'color': 'white'}))

        # Gráfico interativo com Plotly
        st.subheader("📈 Gráfico Interativo")
        colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
        if not colunas_numericas.empty:
            coluna_selecionada = st.selectbox("Selecione uma coluna para o gráfico:", colunas_numericas)
            fig = px.line(df, x=df.index, y=coluna_selecionada, title=f"{coluna_selecionada} ao longo do tempo")
            st.plotly_chart(fig)
        else:
            st.warning("Nenhuma coluna numérica disponível para visualização.")

        # Botão para baixar o arquivo
        st.download_button(
            label="📥 Baixar arquivo",
            data=df.to_csv(index=False, sep=";", encoding="latin-1"),
            file_name=arquivo_selecionado,
            mime="text/csv"
        )
else:
    st.warning("Nenhum arquivo processado encontrado!")
