import os
import logging
import requests

def download_files(links, download_dir="arquivos"):
    """Baixa os arquivos ZIP apenas se ainda não existirem na pasta de destino."""
    
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for link in links:
        filename = os.path.join(download_dir, os.path.basename(link))

        if os.path.exists(filename):
            logging.info(f"Arquivo já existe: {filename}. Pulando download.")
            continue  # Pula o download desse arquivo
        
        try:
            response = requests.get(link, stream=True)
            response.raise_for_status()
            
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            logging.info(f"Download concluído: {filename}")
        
        except Exception as e:
            logging.error(f"Erro ao baixar {link}: {e}")

    return True  # Indica que a função executou sem problemas
