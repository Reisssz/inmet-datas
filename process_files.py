import os
import pandas as pd
from treatment_files import load_metadata, load_weather_data

def processar_todos_arquivos(pasta):
    print(f"Verificando a pasta '{pasta}'...")
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.lower().endswith(".csv")]
    print("Arquivos encontrados:", arquivos)
    
    arquivos_processados = set()
    todos_os_dados = []
    
    for arquivo in arquivos:
        if arquivo in arquivos_processados:
            print(f"Arquivo {arquivo} já processado, ignorando...")
            continue
        
        print(f"* Processando: {arquivo}")
        meta_data = load_metadata()
        
        try:
            dados = load_weather_data(arquivo, meta_data)
            print(f"Shape dos dados carregados de {arquivo}: {dados.shape}")
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")
            continue
        
        if not dados.empty:  # Verifica se o DataFrame não está vazio
            todos_os_dados.append(dados)
            arquivos_processados.add(arquivo)
        else:
            print(f"Aviso: O arquivo {arquivo} retornou um DataFrame vazio.")
    
    if todos_os_dados:
        df_final = pd.concat(todos_os_dados, ignore_index=True)
    else:
        df_final = pd.DataFrame()  # Retorna um DataFrame vazio caso nenhum dado tenha sido processado
    
    return df_final

def save_file(pasta="arquivos_extraidos"):
    df_resultado = processar_todos_arquivos(pasta)
    
    if not df_resultado.empty:
        df_resultado.to_csv("dados_processados.csv", index=False, sep=";", encoding="latin-1")
        print("Arquivo 'dados_processados.csv' salvo com sucesso!")
    else:
        print("Nenhum dado foi processado, o arquivo não será salvo.")

# Chamada principal (caso necessário executar diretamente)
if __name__ == "__main__":
    save_file()
