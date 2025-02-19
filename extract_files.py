import os
import zipfile
import logging

def unzip_files(zip_dir="arquivos", extract_dir="arquivos_extraidos"):
    """Extrai arquivos ZIP para uma pasta específica, evitando extrações duplicadas."""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    os.makedirs(extract_dir, exist_ok=True)

    for zip_file in filter(lambda f: f.endswith(".zip"), os.listdir(zip_dir)):
        zip_file_path = os.path.join(zip_dir, zip_file)

        try:
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                for file_name in zip_ref.namelist():
                    extracted_path = os.path.join(extract_dir, os.path.basename(file_name)) 
                    
                    # Verifica se o arquivo já existe para evitar sobrescrita
                    if os.path.exists(extracted_path):
                        logger.info(f"Arquivo já existe: {extracted_path}. Pulando.")
                        continue  

                    with zip_ref.open(file_name) as source, open(extracted_path, "wb") as target:
                        target.write(source.read())

            logger.info(f"Arquivos extraídos de {zip_file} para {extract_dir}")

        except zipfile.BadZipFile:
            logger.error(f"Arquivo corrompido: {zip_file}")
        except Exception as e:
            logger.error(f"Erro ao extrair {zip_file}: {e}")

