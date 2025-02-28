import os
import zipfile
import logging

"""
Extrai arquivos ZIP de um diretório para outro, evitando extrações duplicadas.

A função percorre todos os arquivos `.zip` em um diretório de origem especificado, extrai seu conteúdo para um diretório de destino e garante que arquivos já extraídos não sejam sobrescritos. Caso algum erro ocorra durante o processo de extração (por exemplo, arquivo ZIP corrompido), ele será registrado no log.

Parâmetros:
- zip_dir (str): Caminho do diretório onde estão localizados os arquivos ZIP a serem extraídos. O valor padrão é 'data/arquivos'.
- extract_dir (str): Caminho do diretório onde os arquivos extraídos serão salvos. O valor padrão é 'data/arquivos_extraidos'.

Comportamento:
- Se o diretório de origem não existir, a função irá gerar um log de erro e interromper a execução.
- Se o diretório de extração não existir, ele será criado automaticamente.
- A função evitará extrair arquivos que já existam no diretório de destino, registrando um log sobre a duplicação.

Exceções:
- Se um arquivo ZIP estiver corrompido, a função gera um log de erro específico.
- Outros erros durante o processo de extração serão registrados no log com uma mensagem de erro.

Exemplo de uso:
- unzip_files("data/arquivos", "data/arquivos_extraidos")
"""


def unzip_files(zip_dir="data/arquivos", extract_dir="data/arquivos_extraidos"):
    """Extrai arquivos ZIP para uma pasta específica, evitando extrações duplicadas."""

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Verifica se o diretório de origem existe
    if not os.path.exists(zip_dir):
        logger.error(f"O diretório {zip_dir} não existe. Nenhum arquivo ZIP encontrado.")
        return

    # Cria o diretório de extração se não existir
    os.makedirs(extract_dir, exist_ok=True)

    # Filtra arquivos .zip no diretório
    arquivos_zip = list(filter(lambda f: f.endswith(".zip"), os.listdir(zip_dir)))
    if not arquivos_zip:
        logger.warning(f"Nenhum arquivo ZIP encontrado em {zip_dir}.")
        return

    for zip_file in arquivos_zip:
        zip_file_path = os.path.join(zip_dir, zip_file)
        logger.info(f"Iniciando a extração do arquivo ZIP: {zip_file_path}")

        try:
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                for file_name in zip_ref.namelist():
                    # Define o caminho do arquivo extraído diretamente na pasta de destino
                    extracted_path = os.path.join(extract_dir, os.path.basename(file_name))  # Usa apenas o nome do arquivo

                    # Verifica se o arquivo já existe para evitar sobrescrita
                    if os.path.exists(extracted_path):
                        logger.info(f"Arquivo já extraído: {extracted_path}. Pulando.")
                        continue

                    # Extrai o arquivo
                    with zip_ref.open(file_name) as source, open(extracted_path, "wb") as target:
                        target.write(source.read())

            logger.info(f"Arquivos extraídos de {zip_file} para {extract_dir}")

        except zipfile.BadZipFile:
            logger.error(f"Arquivo corrompido: {zip_file}")
        except Exception as e:
            logger.error(f"Erro ao extrair {zip_file}: {e}")
