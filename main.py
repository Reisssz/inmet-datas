import logging
import subprocess
from collect_link import collect_links
from download_files import download_files
from extract_files import unzip_files
from process_files import save_file

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    pasta_arquivos = "data/arquivos"
    pasta_extract = "data/arquivos_extraidos"

    # Coletar links dos arquivos ZIP
    links = collect_links()
    if not links:
        logging.warning("Nenhum link encontrado.")
        return

    # Realizar o download dos arquivos
    download_files(links)

    # Extrair os arquivos ZIP (corrigido para passar os dois diretórios corretamente)
    unzip_files(pasta_arquivos, pasta_extract)

    # Processar os arquivos extraídos (corrigido para passar a pasta correta)
    save_file(pasta_extract)

    # Abrir o Streamlit automaticamente
    logging.info("Abrindo painel do Streamlit...")

    try:
        # Comando para rodar o Streamlit no subprocesso
        subprocess.run([r"C:/Users/e1051797/Desktop/inmet_data/venv/Scripts/python.exe", "-m", "streamlit", "run", "app.py"])
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao iniciar o Streamlit: {e}")
    except FileNotFoundError:
        logging.error("Não foi possível encontrar o arquivo app.py. Verifique o caminho."   )
    except Exception as e:
        logging.error(f"Ocorreu um erro ao tentar abrir o Streamlit: {e}")
    
if __name__ == "__main__":
    main()
