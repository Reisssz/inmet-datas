import logging
import os
import re
from weather.utils.collect_link import collect_links
from weather.utils.download_files import download_files
from weather.processing.process_files import save_file
from weather.processing.treatment_files import load_weather_data, extract_metadata, save_to_csv
from weather.database.data_base import concatenate_and_save_to_db
from weather.config.config import PASTA_ARQUIVOS, PASTA_EXTRACT, PASTA_PROCESSADOS, DB_PATH, TABLE_NAME, OUTPUT_FOLDER, INPUT_FOLDER
from weather.utils.extract_files import unzip_files

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    try:
        extract_metadata()
        logging.info("Metadados extraídos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao extrair os metadados: {e}")
        return

    # Processar os arquivos extraídos
    try:
        save_file(PASTA_EXTRACT)
        logging.info("Arquivos processados com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao processar os arquivos: {e}")
        return

    # Cria a pasta de saída, se não existir
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Verifica se a pasta de entrada existe
    if not os.path.exists(INPUT_FOLDER):
        print(f"Erro: A pasta de entrada '{INPUT_FOLDER}' não existe.")
    else:
        # Lista todos os arquivos que seguem o padrão INMET_*.CSV
        files_to_process = [
            f for f in os.listdir(INPUT_FOLDER) if re.match(r'INMET_[A-Z]+_[A-Z]{2}_[A-Z0-9]+_.*?_\d{2}-\d{2}-\d{4}_A_\d{2}-\d{2}-\d{4}\.CSV', f, re.IGNORECASE)
        ]

        # Processa cada arquivo
        for file_name in files_to_process:
            input_file_path = os.path.join(INPUT_FOLDER, file_name)
            output_file_path = os.path.join(OUTPUT_FOLDER, file_name)  # Mantém extensão .CSV

            # Se já foi processado, pula
            if os.path.exists(output_file_path):
                print(f"Arquivo já processado, pulando: {file_name}")
                continue

            # Extrai metadados e processa os dados
            meta_data = extract_metadata(input_file_path)

            if not meta_data.empty:
                weather_data = load_weather_data(input_file_path, meta_data)
                save_to_csv(weather_data, output_file_path)
                print(f"Arquivo salvo com sucesso: {output_file_path}")
            else:
                print(f"Falha ao processar: {file_name}")

        print("✅ Processamento concluído!")

    # Tratar os arquivos e salvar no formato final
    try:
        load_weather_data(PASTA_EXTRACT, PASTA_PROCESSADOS)
        logging.info("Arquivos tratados e salvos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao tratar os arquivos meteorológicos: {e}")
        return

    # Concatenar os arquivos processados e salvar no banco de dados
    try:
        concatenate_and_save_to_db(PASTA_PROCESSADOS, DB_PATH, TABLE_NAME)
        logging.info("Dados salvos no banco de dados SQLite.")
    except Exception as e:
        logging.error(f"Erro ao salvar os dados no banco de dados: {e}")
        return

if __name__ == "__main__":
    main()
