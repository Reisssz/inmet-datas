import os
import logging
import pandas as pd
import re
from datetime import datetime
from src.treatment_files import extract_metadata, load_weather_data

"""
Este módulo contém funções para processar arquivos meteorológicos extraídos em formato CSV. O fluxo de trabalho inclui a coleta de arquivos com base no ano, o processamento dos dados e a geração de novos arquivos CSV com dados limpos e formatados.

1. `obter_ano_arquivo(nome_arquivo)`:
   - Extrai o ano de um arquivo CSV a partir do nome do arquivo usando uma expressão regular.
   
2. `processar_todos_arquivos(pasta, pasta_saida)`:
   - Processa todos os arquivos CSV na pasta de entrada que pertencem aos últimos 10 anos, validando e processando seus dados.
   - Verifica se o arquivo já foi processado (presente na pasta de saída) para evitar duplicação.
   - Os dados processados são salvos em uma pasta de saída especificada.

3. `save_file(pasta="data/arquivos_extraidos", pasta_saida="data/arquivos_processados")`:
   - Função principal para iniciar o processamento dos arquivos.
   - Chama `processar_todos_arquivos` para processar os arquivos extraídos e salva os resultados na pasta de saída.
   - Registra logs detalhados sobre o processo, incluindo arquivos processados, ignorados e erros encontrados.

Dependências:
- `extract_metadata()`: Extrai os metadados necessários do nome do arquivo e do conteúdo CSV.
- `load_weather_data()`: Carrega e processa os dados meteorológicos dos arquivos CSV.

Exceções:
- Caso ocorram erros durante o processamento, eles são registrados no log, mas o fluxo não é interrompido.

Exemplo de uso:
- Para processar arquivos extraídos e salvá-los, basta chamar `save_file()`.
"""

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
            meta_data = extract_metadata(arquivo)
            if meta_data is None:
                logger.error(f"Não foi possível extrair metadados. O arquivo {arquivo} não será processado.")
                continue

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
