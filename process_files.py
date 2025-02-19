import os
import pandas as pd
from treatment_files import load_metadata
from treatment_files import load_weather_data

def processar_todos_arquivos(pasta):
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(".CSV")]
    todos_os_dados = []
    
    for arquivo in arquivos:
        print(f"*Processando: {arquivo}")
        meta_data = load_metadata()
        dados = load_weather_data(arquivo, meta_data)
        todos_os_dados.append(dados)
    
    # Concatenando todos os DataFrames em um único
    df_final = pd.concat(todos_os_dados, ignore_index=True)
    
    return df_final

def save_file(pasta):
    # Exemplo de chamada da função
    pasta = "arquivos_extraidos"
    df_resultado = processar_todos_arquivos(pasta)

    # Para salvar o resultado em um arquivo CSV, se necessário
    df_resultado.to_csv("dados_processados.csv", index=False, sep=";", encoding="latin-1")
