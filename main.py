import logging
from collect_link import collect_links
from download_files import download_files
from extract_files import unzip_files
from process_files import save_file
from treatment_files import load_weather_data
from data_base import concatenate_and_save_to_db

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    pasta_arquivos = "data/arquivos"
    pasta_extract = "data/arquivos_extraidos"
    pasta_processados = "data/arquivos_processados"
    db_path = "data/database_inmet.db"
    table_name = "dados_meteorologicos"

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
        unzip_files(pasta_arquivos, pasta_extract)
        logging.info("Arquivos extraídos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao extrair os arquivos: {e}")
        return

    # Processar os arquivos extraídos
    try:
        save_file(pasta_extract)
        logging.info("Arquivos processados com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao processar os arquivos: {e}")
        return

    # Tratar os arquivos e salvar no formato final
    try:
        load_weather_data(pasta_extract, pasta_processados)
        logging.info("Arquivos tratados e salvos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao tratar os arquivos meteorológicos: {e}")
        return

    # Concatenar os arquivos processados e salvar no banco de dados
    try:
        concatenate_and_save_to_db(pasta_processados, db_path, table_name)
        logging.info("Dados salvos no banco de dados SQLite.")
    except Exception as e:
        logging.error(f"Erro ao salvar os dados no banco de dados: {e}")
        return

if __name__ == "__main__":
    main()
