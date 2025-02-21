import os
import logging
import pandas as pd
import re
from datetime import datetime
from treatment_files import load_metadata, load_weather_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def obter_ano_arquivo(nome_arquivo):
    """Extrai o ano do nome do arquivo usando regex."""
    match = re.search(r'(\d{4})', nome_arquivo)  # Procura um ano (4 dígitos)
    return int(match.group(1)) if match else None

def processar_todos_arquivos(pasta, pasta_saida):
    ano_atual = datetime.now().year
    anos_validos = set(range(ano_atual - 1, ano_atual + 1))  # Últimos 2 anos

    arquivos = [
        os.path.join(pasta, f)
        for f in os.listdir(pasta)
        if f.endswith(".CSV") and obter_ano_arquivo(f) in anos_validos
    ]

    if not arquivos:
        logger.info("Nenhum arquivo dentro do intervalo de anos válidos foi encontrado.")
        return

    # Cria a pasta de saída caso não exista
    os.makedirs(pasta_saida, exist_ok=True)

    arquivos_processados = 0
    arquivos_ignorados = 0

    for arquivo in arquivos:
        nome_arquivo_saida = os.path.join(pasta_saida, os.path.basename(arquivo))

        # Verifica se o arquivo já foi processado (se já existe na pasta de saída)
        if os.path.exists(nome_arquivo_saida):
            logger.info(f"Arquivo já processado: {nome_arquivo_saida}. Pulando.")
            arquivos_ignorados += 1
            continue  # Pula para o próximo arquivo

        logger.info(f"Processando: {arquivo}")
        try:
            meta_data = load_metadata()
            dados = load_weather_data(arquivo, meta_data)

            if not isinstance(dados, pd.DataFrame):
                logger.error(f"Erro: O arquivo {arquivo} não retornou um DataFrame válido.")
                continue

            if dados.empty:
                logger.warning(f"Aviso: O arquivo {arquivo} está vazio.")
                continue

            # Normaliza os nomes das colunas removendo espaços extras
            dados.columns = dados.columns.str.strip()

            # Salva o DataFrame individualmente
            dados.to_csv(nome_arquivo_saida, index=False, sep=";", encoding="latin-1")
            logger.info(f"Arquivo salvo com sucesso: {nome_arquivo_saida}")
            arquivos_processados += 1

        except Exception as e:
            logger.error(f"Erro ao processar {arquivo}: {e}")

    return arquivos_processados, arquivos_ignorados

def save_file(pasta="data/arquivos_extraidos", pasta_saida="data/arquivos_processados"):
    try:
        logger.info("Iniciando o processamento dos arquivos...")
        arquivos_processados, arquivos_ignorados = processar_todos_arquivos(pasta, pasta_saida)

        # Log de resumo após o processamento
        if arquivos_processados > 0:
            logger.info(f"{arquivos_processados} arquivos processados com sucesso.")
        if arquivos_ignorados > 0:
            logger.info(f"{arquivos_ignorados} arquivos foram ignorados (já estavam processados).")
        if arquivos_processados == 0 and arquivos_ignorados == 0:
            logger.info("Nenhum arquivo foi processado.")

    except Exception as e:
        logger.error(f"Erro ao processar arquivos: {e}")
