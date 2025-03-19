import os
import zipfile
import logging
from weather.config.config import FOLDER_MAIN,EXTRACT_FOLDER


def unzip_files():
    """Extrai arquivos ZIP para uma pasta específica, evitando extrações duplicadas."""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Verifica se o diretório de origem existe
    if not os.path.exists(FOLDER_MAIN):
        logger.error(f"O diretório {FOLDER_MAIN} não existe. Nenhum arquivo ZIP encontrado.")
        return

    # Cria o diretório de extração se não existir
    os.makedirs(EXTRACT_FOLDER, exist_ok=True)

    # Filtra arquivos .zip no diretório
    arquivos_zip = [f for f in os.listdir(FOLDER_MAIN) if f.lower().endswith(".zip")]
    if not arquivos_zip:
        logger.warning(f"Nenhum arquivo ZIP encontrado em {FOLDER_MAIN}.")
        return

    for zip_file in arquivos_zip:
        zip_file_path = os.path.join(FOLDER_MAIN, zip_file)
        logger.info(f"Iniciando a extração do arquivo ZIP: {zip_file_path}")

        try:
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                # Lista os arquivos dentro do ZIP
                for file_name in zip_ref.namelist():
                    extracted_path = os.path.join(EXTRACT_FOLDER, file_name)

                    # Evita sobrescrever arquivos já extraídos
                    if os.path.exists(extracted_path):
                        logger.info(f"Arquivo já extraído: {extracted_path}. Pulando.")
                        continue

                    # Cria diretórios necessários
                    os.makedirs(os.path.dirname(extracted_path), exist_ok=True)

                    # Extrai o arquivo
                    zip_ref.extract(file_name, EXTRACT_FOLDER)

            logger.info(f"Arquivos extraídos com sucesso de {zip_file} para {EXTRACT_FOLDER}")

        except zipfile.BadZipFile:
            logger.error(f"Arquivo corrompido: {zip_file_path}")
        except Exception as e:
            logger.error(f"Erro ao extrair {zip_file_path}: {e}")

