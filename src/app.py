import streamlit as st

# Configuração da página
st.set_page_config(page_title="Painel de Arquivos Processados", layout="wide")

import logging
import os
import pandas as pd


# Comentário explicativo (antes era uma docstring)
# Este script cria uma interface no Streamlit para visualizar e baixar arquivos CSV processados.
# Funções:
# 1. listar_arquivos():
#    - Objetivo: Lista todos os arquivos CSV na pasta de arquivos processados (sem subpastas).
#    - Retorno: Uma lista contendo os nomes dos arquivos CSV encontrados na pasta.
#
# 2. carregar_dados(arquivo):
#    - Objetivo: Carrega um arquivo CSV da pasta de processados em um DataFrame.
#    - Parâmetros:
#      - arquivo (str): Nome do arquivo CSV a ser carregado.
#    - Retorno: Um DataFrame contendo os dados do arquivo, ou None em caso de erro.
#
# Interface do Streamlit:
# - Exibe um painel onde o usuário pode selecionar um arquivo CSV processado.
# - Mostra os dados do arquivo selecionado em um DataFrame.
# - Disponibiliza um botão para baixar o arquivo CSV.

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho relativo onde estão os arquivos processados
PASTA_PROCESSADOS = r"C:/Users/e1051797/Desktop/inmet_data/data/arquivos_processados"

def listar_arquivos():
    """Lista os arquivos CSV na pasta de processados (sem subpastas)"""
    if not os.path.exists(PASTA_PROCESSADOS):
        logging.error(f"A pasta {PASTA_PROCESSADOS} não foi encontrada!")
        return []
    
    # Lista os arquivos diretamente dentro da pasta
    arquivos_csv = [f for f in os.listdir(PASTA_PROCESSADOS) if f.lower().endswith(".csv")]
    
    logging.info(f"Arquivos encontrados: {arquivos_csv}")  # Log dos arquivos encontrados
    logging.info(f"Caminho da pasta: {PASTA_PROCESSADOS}")  # Log do caminho da pasta
    return arquivos_csv

def carregar_dados(arquivo):
    """Carrega um arquivo CSV em um DataFrame"""
    caminho_arquivo = os.path.join(PASTA_PROCESSADOS, arquivo)
    logging.info(f"Tentando carregar o arquivo: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo, sep=";", encoding="latin-1")
        return df
    except Exception as e:
        logging.error(f"Erro ao carregar o arquivo {arquivo}: {e}")
        return None

# Interface do Streamlit
st.title("📊 Painel de Arquivos Processados")

# Lista os arquivos disponíveis
arquivos = listar_arquivos()

if arquivos:
    arquivo_selecionado = st.selectbox("Selecione um arquivo para visualizar:", arquivos)

    # Carrega e exibe os dados
    df = carregar_dados(arquivo_selecionado)
    if df is not None:
        st.write(f"**Visualizando: {arquivo_selecionado}**")
        st.dataframe(df)

        # Botão para baixar o arquivo
        st.download_button(
            label="📥 Baixar arquivo",
            data=df.to_csv(index=False, sep=";", encoding="latin-1"),
            file_name=arquivo_selecionado,
            mime="text/csv"
        )
else:
    st.warning("Nenhum arquivo processado encontrado!")
