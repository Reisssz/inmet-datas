import logging
from weather.utils.collect_link import collect_links
from weather.utils.download_files import download_files
from weather.utils.extract_files import unzip_files
from weather.processing.process_files import save_file
from weather.config.config import PROCESS_FOLDER,EXTRACT_FOLDER
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
"""
    # Criar a pasta de saída, se não existir
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    # Verificar se a pasta de entrada existe
    if not os.path.exists(FILES_FOLDER):
        logging.error(f"Erro: A pasta de entrada '{FILES_FOLDER}' não existe.")
        return

    # Listar todos os arquivos a serem processados
    files_to_process = [
        f for f in os.listdir(FILES_FOLDER) if re.match(
            r'INMET_[A-Z]+_[A-Z]{2}_[A-Z0-9]+_.*?_\d{2}-\d{2}-\d{4}_A_\d{2}-\d{2}-\d{4}\.CSV', f, re.IGNORECASE
        )
    ]

    if not files_to_process:
        logging.warning("Nenhum arquivo de dados encontrado para processamento.")
        return

    # Processar cada arquivo
    for file_name in files_to_process:
        input_file_path = os.path.join(FILES_FOLDER, file_name)
        output_file_path = os.path.join(PROCESSED_FOLDER, file_name)  # Mantém extensão .CSV

        # Se já foi processado, pula
        if os.path.exists(output_file_path):
            logging.info(f"Arquivo já processado, pulando: {file_name}")
            continue

        # Extrair metadados do arquivo específico
        meta_data = extract_metadata(input_file_path)
        if meta_data.empty:
            logging.warning(f"Metadados não extraídos corretamente: {file_name}")
            continue

        # Carregar e processar os dados meteorológicos
        weather_data = load_weather_data(input_file_path, meta_data)
        if weather_data.empty:
            logging.warning(f"Falha ao processar os dados meteorológicos: {file_name}")
            continue

        # Salvar os dados processados
        save_to_csv(weather_data, output_file_path)
        logging.info(f"Arquivo salvo com sucesso: {output_file_path}")

    logging.info("✅ Processamento concluído!")

    # Concatenar os arquivos processados e salvar no banco de dados
    try:
        concatenate_and_save_to_db(PROCESSED_FOLDER, DB_PATH, TABLE_NAME)
        logging.info("Dados salvos no banco de dados SQLite.")
    except Exception as e:
        logging.error(f"Erro ao salvar os dados no banco de dados: {e}") """

if __name__ == "__main__":
    main()
