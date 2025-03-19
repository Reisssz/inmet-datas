import os
import logging
import pandas as pd
from weather.processing.treatment_files import extract_metadata, load_weather_data

"""
Módulo atualizado para processar TODOS os arquivos CSV sem filtro de ano.

Correções:
✅ Removeu filtro por ano, processando qualquer arquivo CSV encontrado.
✅ Adicionou verificação para evitar erro de `NoneType`.
✅ Logs aprimorados para melhor depuração.
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def processar_todos_arquivos(pasta, pasta_saida):
    # Exibe os arquivos encontrados na pasta
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(".CSV")]

    if not arquivos:
        logger.warning("Nenhum arquivo CSV encontrado para processamento.")
        return 0, 0  # Retorna zeros para evitar erro de unpacking

    arquivos_processados = 0
    arquivos_ignorados = 0

    for arquivo in arquivos:
        nome_arquivo_saida = os.path.join(pasta_saida, os.path.basename(arquivo))

        # Pular arquivos já processados
        if os.path.exists(nome_arquivo_saida):
            logger.info(f"Arquivo já processado: {nome_arquivo_saida}. Pulando.")
            arquivos_ignorados += 1
            continue

        logger.info(f"Processando: {arquivo}")

        try:
            meta_data = extract_metadata()  # Corrigido: Passa o caminho do arquivo
            if meta_data is None or meta_data.empty:
                logger.error(f"Não foi possível extrair metadados. O arquivo {arquivo} será ignorado.")
                continue

            dados = load_weather_data(meta_data)

            if not isinstance(dados, pd.DataFrame) or dados.empty:
                logger.error(f"Erro: O arquivo {arquivo} não contém dados válidos.")
                continue

            # Normaliza os nomes das colunas
            dados.columns = dados.columns.str.strip()

            # Salva o DataFrame processado
            dados.to_csv(nome_arquivo_saida, index=False, sep=";", encoding="latin-1")
            logger.info(f"Arquivo salvo com sucesso: {nome_arquivo_saida}")
            arquivos_processados += 1

        except Exception as e:
            logger.error(f"Erro ao processar {arquivo}: {e}")

    return arquivos_processados, arquivos_ignorados

def save_file(EXTRACT_FOLDER,PROCESS_FOLDER):
    """Inicia o processamento dos arquivos sem filtro de ano."""
    

    try:
        logger.info("Iniciando o processamento dos arquivos...")

        # Criar as pastas se não existirem
        os.makedirs(EXTRACT_FOLDER, exist_ok=True)
        os.makedirs(PROCESS_FOLDER, exist_ok=True)

        arquivos_processados, arquivos_ignorados = processar_todos_arquivos(EXTRACT_FOLDER, PROCESS_FOLDER)

        if arquivos_processados > 0:
            logger.info(f"{arquivos_processados} arquivos processados com sucesso.")
        if arquivos_ignorados > 0:
            logger.info(f"{arquivos_ignorados} arquivos foram ignorados (já estavam processados).")
        if arquivos_processados == 0 and arquivos_ignorados == 0:
            logger.info("Nenhum arquivo foi processado.")

    except Exception as e:
        logger.error(f"Erro ao processar arquivos: {e}")
