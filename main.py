import logging
import os
import pandas as pd
from collect_link import collect_links
from download_files import download_files
from extract_files import unzip_files
from process_files import save_file

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    pasta = "arquivos_tratados"
    os.makedirs(pasta, exist_ok=True)

        # Coletar links dos arquivos ZIP
    links = collect_links()
    if not links:
            logging.warning("Nenhum link encontrado.")
            return

        # Realizar o download dos arquivos
    download_files(links)
        
        # Extrair os arquivos ZIP
    unzip_files()

    save_file(pasta)
    

if __name__ == "__main__":
    main()
