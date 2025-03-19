import pandas as pd
import numpy as np
import re
from weather.config.config import PROCESS_FOLDER,EXTRACT_FILE

# Função para extrair metadados do arquivo
def extract_metadata():
    with open(EXTRACT_FILE) as f:
        lines = f.readlines()[:8]  # Lê apenas as primeiras linhas, onde estão os metadados

    metadata_dict = {}
    for line in lines:
        if ":;" in line:
            key, value = line.strip().split(":;", 1)
            metadata_dict[key.strip()] = value.strip()

    match = re.search(r'INMET_([A-Z]+)_([A-Z]{2})_([A-Z0-9]+)_(.*?)_(\d{2}-\d{2}-\d{4})_A_\d{2}-\d{2}-\d{4}\.CSV', EXTRACT_FILE, re.IGNORECASE)
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
def load_weather_data(meta_data):
    try:
        main_data = pd.read_csv(EXTRACT_FILE, sep=";", encoding="latin-1", decimal=",", skiprows=8)

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
        print(f"Erro ao processar {EXTRACT_FILE}: {e}")
        return pd.DataFrame()

# Função para salvar o DataFrame em um arquivo CSV na pasta de arquivos processados
def save_to_csv(df, filename):
    output_file = f"{PROCESS_FOLDER}/{filename}"
    df.to_csv(output_file, index=False, sep=";", encoding="utf-8", decimal=",")
    print(f"Arquivo salvo em: {output_file}")

# Extraindo metadados e processando os dados
meta_data = extract_metadata()
if not meta_data.empty:
    weather_data = load_weather_data(meta_data)
    if not weather_data.empty:
        save_to_csv(weather_data, "dados_processados.csv")
    else:
        print("Erro: Nenhum dado meteorológico processado.")
else:
    print("Erro: meta_data não foi extraído corretamente.")
