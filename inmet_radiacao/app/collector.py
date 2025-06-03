def executar_coleta():
    from core.collect_link import coletar_links
    from core.download_files import baixar_arquivos
    from core.extract_files import unzip_files
    from core.process_files import save_file

    coletar_links()
    baixar_arquivos()
    unzip_files()
    save_file()
