import os
import logging
import requests

def download_files(links, download_dir="arquivos"):
    """Baixa arquivos ZIP apenas se ainda não existirem na pasta de destino."""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    os.makedirs(download_dir, exist_ok=True)

    for link in links:
        filename = os.path.join(download_dir, os.path.basename(link))

        if os.path.exists(filename):
            logger.info(f"Já existe: {filename}. Pulando.")
            continue  

        try:
            with requests.get(link, stream=True) as response:
                response.raise_for_status()
                with open(filename, "wb") as file:
                    for chunk in response.iter_content(8192):
                        file.write(chunk)

            logger.info(f"Download concluído: {filename}")

        except requests.RequestException as e:
            logger.error(f"Erro ao baixar {link}: {e}")

    return True  # Indica execução bem-sucedida
