import pandas as pd
import numpy as np
import re
import os
from config import input_folder, output_folder

# Função para extrair metadados do arquivo
def extract_metadata(file_path):
    with open(file_path, "r", encoding="latin-1") as f:
        lines = f.readlines()[:8]  # Lê apenas as primeiras linhas, onde estão os metadados

    metadata_dict = {}
    for line in lines:
        if ":;" in line:
            key, value = line.strip().split(":;", 1)
            metadata_dict[key.strip()] = value.strip()

    match = re.search(r'INMET_([A-Z]+)_([A-Z]{2})_([A-Z0-9]+)_(.*?)_(\d{2}-\d{2}-\d{4})_A_\d{2}-\d{2}-\d{4}\.CSV', file_path, re.IGNORECASE)
    if not match:
        return pd.DataFrame()

    regiao, uf, codigo, estacao, data_fundacao = match.groups()

    def safe_float(value):
        """Converte para float, tratando erros e substituindo valores inválidos por np.nan"""
        try:
            return float(value.replace(",", "."))
        except (ValueError, AttributeError):
            return np.nan

    return pd.DataFrame({
        "DATA DE FUNDAÇÃO (YYYY-MM-DD)": [data_fundacao.replace("-", "/")],
        "CODIGO (WMO)": [metadata_dict.get("CODIGO (WMO)", codigo)],
        "REGIÃO": [metadata_dict.get("REGIÃO", regiao)],
        "UF": [metadata_dict.get("UF", uf)],
        "ESTAÇÃO": [metadata_dict.get("ESTAÇÃO", estacao)],
        "LATITUDE": [safe_float(metadata_dict.get("LATITUDE"))],
        "LONGITUDE": [safe_float(metadata_dict.get("LONGITUDE"))],
        "ALTITUDE": [safe_float(metadata_dict.get("ALTITUDE"))]
    })

# Função para carregar os dados meteorológicos e adicionar metadados
def load_weather_data(file_path, meta_data):
    try:
        main_data = pd.read_csv(file_path, sep=";", encoding="latin-1", decimal=",", skiprows=8)

        names_columns = [
            "DATA", "HORA", "PRECIP_TOTAL", "PRESSAO_ATM",
            "PRESSAO_MAX", "PRESSAO_MIN", "RADIACAO",
            "TEMP_AR", "TEMP_ORVALHO", "TEMP_MAX",
            "TEMP_MIN", "TEMP_ORV_MAX", "TEMP_ORV_MIN",
            "UMID_MAX", "UMID_MIN", "UMID_AR",
            "VENTO_DIR", "VENTO_RAJADA", "VENTO_VEL"
        ]

        main_data = main_data.iloc[:, :len(names_columns)]
        main_data.columns = names_columns
        main_data.replace(-9999, np.nan, inplace=True)

        main_data["DATA_HORA"] = pd.to_datetime(main_data["DATA"] + " " + main_data["HORA"], format="%Y/%m/%d %H%M UTC", errors='coerce')
        main_data.drop(columns=["DATA", "HORA"], errors='ignore', inplace=True)
        
        for column in meta_data.columns:
            main_data[column] = meta_data[column].iloc[0]

        columns_order = list(meta_data.columns) + [col for col in main_data.columns if col not in meta_data.columns]
        return main_data[columns_order]

    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return pd.DataFrame()

# Função para salvar o DataFrame em um arquivo CSV
def save_to_csv(df, output_file):
    df.to_csv(output_file, index=False, sep=";", encoding="utf-8", decimal=",")

# Cria a pasta de saída, se não existir
os.makedirs(output_folder, exist_ok=True)

# Verifica se a pasta de entrada existe
if not os.path.exists(input_folder):
    print(f"Erro: A pasta de entrada '{input_folder}' não existe.")
else:
    # Lista todos os arquivos que seguem o padrão INMET_*.CSV
    files_to_process = [f for f in os.listdir(input_folder) if re.match(r'INMET_[A-Z]+_[A-Z]{2}_[A-Z0-9]+_.*?_\d{2}-\d{2}-\d{4}_A_\d{2}-\d{2}-\d{4}\.CSV', f, re.IGNORECASE)]

    # Processa cada arquivo
    for file_name in files_to_process:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name)  # Mantém extensão .CSV

        # Se já foi processado, pula
        if os.path.exists(output_file_path):
            print(f"Arquivo já processado, pulando: {file_name}")
            continue

        # Extrai metadados e processa os dados
        meta_data = extract_metadata(input_file_path)

        if not meta_data.empty:
            weather_data = load_weather_data(input_file_path, meta_data)
            save_to_csv(weather_data, output_file_path)
            print(f"Arquivo salvo com sucesso: {output_file_path}")
        else:
            print(f"Falha ao processar: {file_name}")

    print("✅ Processamento concluído!")
