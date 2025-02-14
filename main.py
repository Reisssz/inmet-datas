import logging
import os
from collect_link import collect_links
from extract_files import unzip_files
from treatment_files import process_and_convert_to_excel
from download_files import download_files

def main():
    """Executa o fluxo principal de download e extração."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("🚀 Iniciando o processo...")

    try:
        # Diretórios
        extract_dir = r"C:\Users\e1051797\Desktop\inmet_data\arquivos_extraidos"
        output_dir = "dados_tratados"

        # Coleta os links
        links = collect_links()
        
        if not isinstance(links, list) or not links:
            logging.error("❌ Nenhum link válido foi encontrado. Encerrando o processo.")
            return

        logging.info(f"🔗 Links encontrados: {links}")

        # Verifica se os arquivos já existem antes de baixar
        if not os.path.exists(extract_dir) or not any(os.scandir(extract_dir)):
            logging.info("📥 Iniciando download dos arquivos...")
            status = download_files(links)
            
            if not status:
                logging.error("❌ Erro: Um ou mais arquivos não foram baixados.")
                return

            logging.info("📂 Extraindo arquivos ZIP...")
            unzip_files()
        else:
            logging.info("✅ Os arquivos já foram baixados e extraídos. Pulando esta etapa.")

        # Verifica se os arquivos CSV existem antes de iniciar o processamento
        if os.path.exists(extract_dir) and any(os.scandir(extract_dir)):
            logging.info("🔄 Iniciando processamento dos dados...")
            process_and_convert_to_excel(extract_dir, output_dir)
            logging.info("✅ Processamento concluído!")
        else:
            logging.error(f"🚨 Nenhum arquivo CSV encontrado dentro de {extract_dir}. Verifique a extração.")

    except Exception as e:
        logging.error(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
