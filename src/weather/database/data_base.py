import os
import pandas as pd
import sqlite3
import unidecode
from weather.config.config import DB_FOLDER, DB_PATH, TABLE_NAME, PROCESSED_DATA_DIR

def find_all_csv_files(folder):
    """Busca recursivamente por arquivos CSV na pasta especificada."""
    csv_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    return csv_files

def normalize_column_names(columns):
    """Remove acentos, caracteres especiais e limita os nomes a 30 caracteres."""
    new_columns = {}
    for col in columns:
        new_col = col.replace("(YYYY-MM-DD)", "").strip()  # Remove trecho indesejado
        new_col = unidecode.unidecode(new_col)  # Remove acentos
        new_col = new_col.replace(" ", "_").replace("(", "").replace(")", "").lower()
        new_columns[col] = new_col[:30]  # Limita a 30 caracteres
    return new_columns

def read_csv_safely(file_path):
    """Tenta ler um arquivo CSV ajustando automaticamente o separador."""
    try:
        df = pd.read_csv(file_path, sep=";", encoding="latin-1", decimal=",", na_values=["", " "])
        return df
    except pd.errors.ParserError:
        try:
            df = pd.read_csv(file_path, sep=",", encoding="latin-1", decimal=",", na_values=["", " "])
            return df
        except pd.errors.ParserError:
            print(f"Erro ao analisar CSV (verifique o delimitador): {file_path}")
            return None

def concatenate_and_save_to_db():
    """Concatena todos os arquivos CSV da pasta processada e salva no banco de dados."""
    
    if not os.path.exists(PROCESSED_DATA_DIR):
        print(f"Pasta não encontrada: {PROCESSED_DATA_DIR}")
        return

    csv_files = find_all_csv_files(PROCESSED_DATA_DIR)
    if not csv_files:
        print("Nenhum arquivo CSV encontrado para processamento.")
        return

    all_dataframes = []

    for file_path in csv_files:
        if os.path.getsize(file_path) < 10:  # Verifica se o arquivo está vazio
            print(f"Arquivo vazio ou corrompido: {file_path}")
            continue

        df = read_csv_safely(file_path)
        if df is None or df.empty or df.columns.size == 0:
            print(f"Arquivo sem dados úteis: {file_path}")
            continue

        # Normaliza os nomes das colunas
        column_mapping = normalize_column_names(df.columns)
        df.rename(columns=column_mapping, inplace=True)

        all_dataframes.append(df)

    if not all_dataframes:
        print("Nenhum dado válido foi encontrado para salvar no banco de dados.")
        return

    # Concatena todos os DataFrames
    final_df = pd.concat(all_dataframes, ignore_index=True)

    # Salva no banco SQLite
    try:
        with sqlite3.connect(DB_PATH) as conn:
            final_df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
            print(f"Dados salvos no banco de dados SQLite na tabela '{TABLE_NAME}'.")
    except Exception as e:
        print(f"Erro ao salvar os dados no banco de dados: {e}")
