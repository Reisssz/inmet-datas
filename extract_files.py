import os
import zipfile
import logging

def unzip_files(zip_dir="arquivos", extract_dir="arquivos_extraidos"):
    """Extrai os arquivos ZIP apenas se ainda não tiverem sido extraídos."""
    
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    for zip_file in os.listdir(zip_dir):
        if zip_file.endswith(".zip"):
            zip_file_path = os.path.join(zip_dir, zip_file)
            zip_folder_name = os.path.splitext(zip_file)[0]
            zip_extract_path = os.path.join(extract_dir, zip_folder_name)

            if os.path.exists(zip_extract_path):
                logging.info(f"Arquivo já extraído: {zip_extract_path}. Pulando extração.")
                continue  # Pula a extração desse arquivo

            try:
                with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                    zip_ref.extractall(zip_extract_path)

                logging.info(f"Arquivos extraídos para: {zip_extract_path}")

            except zipfile.BadZipFile:
                logging.error(f"Erro ao extrair {zip_file}: arquivo ZIP corrompido.")
            except Exception as e:
                logging.error(f"Erro inesperado ao extrair {zip_file}: {e}")
