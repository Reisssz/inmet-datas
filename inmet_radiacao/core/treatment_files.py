import pandas as pd
import numpy as np
import re
import os
import unicodedata
from config import INPUT_FOLDER, OUTPUT_FOLDER

def extract_metadata(file_path):
    with open(file_path, "r", encoding="latin-1") as f:
        lines = f.readlines()[:8]

    metadata_dict = {}
    for line in lines:
        if ":;" in line:
            key, value = line.strip().split(":;", 1)
            metadata_dict[key.strip()] = value.strip()

    match = re.search(
        r'INMET_([A-Z]+)_([A-Z]{2})_([A-Z0-9]+)_(.*?)_(\d{2}-\d{2}-\d{4})_A_\d{2}-\d{2}-\d{4}\.CSV',
        file_path, re.IGNORECASE
    )
    if not match:
        return pd.DataFrame()

    regiao, uf, codigo, estacao, data_fundacao = match.groups()

    def safe_float(value):
        try:
            return float(value.replace(",", "."))
        except (ValueError, AttributeError):
            return np.nan

    return pd.DataFrame({
        "DATA DE FUNDAÇÃO": [data_fundacao.replace("-", "/")],
        "CODIGO": [metadata_dict.get("CODIGO (WMO)", codigo)],
        "REGIÃO": [metadata_dict.get("REGIÃO", regiao)],
        "UF": [metadata_dict.get("UF", uf)],
        "ESTAÇÃO": [metadata_dict.get("ESTAÇÃO", estacao)],
        "LATITUDE": [safe_float(metadata_dict.get("LATITUDE"))],
        "LONGITUDE": [safe_float(metadata_dict.get("LONGITUDE"))],
        "ALTITUDE": [safe_float(metadata_dict.get("ALTITUDE"))]
    })

def limpar_coluna(col):
    """Remove acentos e caracteres especiais de colunas"""
    return unicodedata.normalize("NFKD", col).encode("ASCII", "ignore").decode("ASCII").upper()

def clean_column_name(col):
    # Remove acentos e caracteres especiais
    col = unicodedata.normalize("NFKD", col).encode("ascii", "ignore").decode("utf-8")
    col = col.upper().strip()
    col = col.replace(" ", "_").replace("__", "_")
    return col

def load_weather_data(file_path, meta_data):
    try:
        if meta_data["UF"].iloc[0] != "PA":
            return pd.DataFrame()

        # Lê os dados, pulando os metadados
        df = pd.read_csv(file_path, sep=";", encoding="latin-1", skiprows=8)

        # Normaliza os nomes das colunas
        df.columns = [clean_column_name(c) for c in df.columns]

        # Identifica a coluna de radiação
        rad_col = next((c for c in df.columns if "RADIACAO_GLOBAL" in c), None)
        if rad_col is None:
            return pd.DataFrame()

        # Usa apenas as colunas necessárias
        if not {"DATA", "HORA_UTC"}.issubset(df.columns):
            return pd.DataFrame()

        df = df[["DATA", "HORA_UTC", rad_col]]
        df.rename(columns={rad_col: "RADIACAO"}, inplace=True)

        # Junta data e hora
        df["DATA_HORA"] = pd.to_datetime(df["DATA"] + " " + df["HORA_UTC"], errors="coerce")
        df.drop(columns=["DATA", "HORA_UTC"], inplace=True)
        df = df.dropna(subset=["DATA_HORA"])

        # Adiciona metadados
        for col in meta_data.columns:
            df[col] = meta_data[col].iloc[0]

        colunas = ["DATA_HORA"] + [col for col in df.columns if col != "DATA_HORA"]
        return df[colunas]

    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return pd.DataFrame()

def save_to_csv(df, output_file):
    df.to_csv(output_file, index=False, sep=";", encoding="utf-8", decimal=",")
