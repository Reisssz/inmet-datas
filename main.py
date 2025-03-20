import logging
import os
import re
from weather.utils.collect_link import collect_links
from weather.utils.download_files import download_files
from weather.utils.extract_files import unzip_files
from weather.processing.process_files import save_file
from weather.database.data_base import concatenate_and_save_to_db
from weather.processing.treatment_files import extract_metadata,save_to_csv,load_weather_data
from weather.config.config import FOLDER_MAIN,FOLDER_MAIN,PROCESS_FOLDER,EXTRACT_FOLDER

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    # Coletar links dos arquivos ZIP
    links = collect_links()
    if not links:
        logging.warning("Nenhum link encontrado.")
        return

    # Realizar o download dos arquivos
    try:
        download_files(links)
        logging.info("Arquivos baixados com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao baixar os arquivos: {e}")
        return
 
    # Extrair os arquivos ZIP
    try:
        unzip_files()
        logging.info("Arquivos extraídos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao extrair os arquivos: {e}")
        return
    # Processar os arquivos extraídos
    try:
        save_file(EXTRACT_FOLDER,PROCESS_FOLDER)
        logging.info("Arquivos processados com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao processar os arquivos: {e}")
        return

    

    # Verificar se a pasta de entrada existe
    if not os.path.exists(FOLDER_MAIN):
        logging.error(f"Erro: A pasta de entrada '{FOLDER_MAIN}' não existe.")
        return

    # Listar todos os arquivos a serem processados
    files_to_process = [
       f for f in os.listdir(PROCESS_FOLDER) if re.match(
            r'INMET_[A-Z]+_[A-Z]{2}_[A-Z0-9]+_.*?_\d{2}-\d{2}-\d{4}_A_\d{2}-\d{2}-\d{4}\.CSV', f, re.IGNORECASE
        )
    ]

    if not files_to_process :
        logging.warning("Nenhum arquivo de dados encontrado para processamento.")
        return


    # Concatenar os arquivos processados e salvar no banco de dados
    try:
        concatenate_and_save_to_db()
        logging.info("Dados salvos no banco de dados SQLite.")
    except Exception as e:
        logging.error(f"Erro ao salvar os dados no banco de dados: {e}")

if __name__ == "__main__":
    main()
