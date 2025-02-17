import logging
import os
import pandas as pd
from collect_link import collect_links
from download_files import download_files
from extract_files import unzip_files
from treatment_files import processar_dados

def processar_e_converter_para_excel(file_path, pasta_tratada):
    try:
        # Tentando abrir o arquivo CSV com uma codificação diferente e delimitador ';'
        df = pd.read_csv(file_path, encoding='ISO-8859-1', delimiter=';', on_bad_lines='skip')

        # Nome do arquivo Excel que será salvo
        nome_arquivo_excel = os.path.basename(file_path).replace('.CSV', '_tratado.xlsx')
        caminho_arquivo_excel = os.path.join(pasta_tratada, nome_arquivo_excel)

        # Salvando o DataFrame como Excel
        df.to_excel(caminho_arquivo_excel, index=False, engine='openpyxl')
        
        # Log de sucesso
        logging.info(f"Arquivo {file_path} convertido e salvo em {caminho_arquivo_excel}")
        
    except Exception as e:
        logging.error(f"Erro ao converter o arquivo {file_path} para Excel: {e}")

def main():
    # Configuração do logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    try:
        # Criação da pasta 'arquivos_tratados' caso não exista
        pasta_tratada = "arquivos_tratados"
        if not os.path.exists(pasta_tratada):
            os.makedirs(pasta_tratada)

        # Coleta os links dos arquivos ZIP
        logger.info("Coletando links dos arquivos...")
        links = collect_links()

        # Log dos links encontrados
        logger.info(f"Links encontrados: {links}")

        if not links:
            logger.warning("Nenhum link encontrado.")
            return

        # Baixa os arquivos ZIP
        logger.info("Baixando arquivos...")
        download_files(links)

        # Extrai os arquivos ZIP
        logger.info("Extraindo arquivos...")
        unzip_files()

        # Verifica o conteúdo da pasta de extração
        logger.info("Verificando conteúdo da pasta 'arquivos_extraidos'...")
        arquivos_extraidos = os.listdir("arquivos_extraidos")
        logger.info(f"Arquivos encontrados: {arquivos_extraidos}")

        # Processa e converte os arquivos CSV para Excel
        logger.info("Processando arquivos CSV...")
        found_csv = False
        for root, dirs, files in os.walk("arquivos_extraidos"):
            logger.info(f"Verificando pasta: {root}")
            for file in files:
                logger.info(f"Arquivo encontrado: {file}")
                if file.endswith(".CSV"):  # Filtra apenas arquivos CSV
                    found_csv = True
                    file_path = os.path.join(root, file)
                    logger.info(f"Processando o arquivo {file_path}...")

                    # Chama a função para processar e converter para Excel
                    processar_e_converter_para_excel(file_path, pasta_tratada)

        if not found_csv:
            logger.warning("Nenhum arquivo CSV encontrado para processamento.")

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
