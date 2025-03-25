import os
import logging
import requests

"""
Baixa arquivos ZIP a partir de uma lista de links, salvando-os em uma pasta de destino especificada.

A função verifica se o arquivo já existe na pasta de destino antes de realizar o download. Se o arquivo já estiver presente, ele será ignorado. Caso contrário, o arquivo será baixado e salvo localmente.

Parâmetros:
- links (list): Lista de URLs para os arquivos ZIP a serem baixados.
- download_dir (str): Caminho da pasta onde os arquivos serão salvos. O valor padrão é 'data/arquivos'.

Retorno:
- True: Indica que a execução foi bem-sucedida.

Exceções:
- Em caso de erro no download, a exceção será registrada no log, e o arquivo será ignorado, mas o processo continuará para os outros arquivos.

Exemplo de uso:
- links = ["https://example.com/arquivo1.zip", "https://example.com/arquivo2.zip"]
- download_files(links)
"""


def download_files(links, download_dir="data/arquivos"):
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
