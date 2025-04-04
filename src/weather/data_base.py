import os
import pandas as pd
import sqlite3
import unidecode
from src.weather.config.config import PROCESSED_FOLDER, DB_PATH, TABLE_NAME


def find_all_csv_files(folder):
    """Busca recursivamente por arquivos CSV em todas as subpastas."""
    csv_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".csv"):  # Considera minúsculas e maiúsculas
                csv_files.append(os.path.join(root, file))
    return csv_files

def normalize_column_names(columns):
    """Remove acentos, caracteres especiais e limita os nomes a 30 caracteres."""
    new_columns = {}
    for col in columns:
        new_col = col.replace("(YYYY-MM-DD)", "").strip()  # Remove o trecho indesejado
        new_col_ascii = unidecode.unidecode(new_col)  # Remove acentos
        new_col_ascii = new_col_ascii.replace(" ", "_").replace("(", "").replace(")", "").lower()
        new_columns[col] = new_col_ascii[:30]  # Limita a 30 caracteres
    return new_columns

def concatenate_and_save_to_db(PROCESSED_FOLDER, DB_PATH, TABLE_NAME):
    files = find_all_csv_files(PROCESSED_FOLDER)

    if not files:
        print("Nenhum arquivo CSV encontrado na pasta processada.")
        return

    dataframes = []
    
    for file_path in files:
        try:
            df = pd.read_csv(file_path, sep=";", encoding="latin-1", decimal=",")
            dataframes.append(df)
            print(f"Arquivo lido com sucesso: {file_path}")
        except Exception as e:
            print(f"Erro ao ler {file_path}: {e}")

    if dataframes:
        final_df = pd.concat(dataframes, ignore_index=True)

        # Renomeia as colunas removendo "(YYYY-MM-DD)" sem mudar o restante
        final_df.rename(columns=normalize_column_names(final_df.columns), inplace=True)

        # Conecta ao banco SQLite
        conn = sqlite3.connect(DB_PATH)
        try:
            final_df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
            print(f"Dados salvos no banco de dados SQLite na tabela '{TABLE_NAME}'.")
        except Exception as e:
            print(f"Erro ao salvar os dados no banco de dados: {e}")
        finally:
            conn.close()
    else:
        print("Nenhum dado foi processado.")

# Executa a função
concatenate_and_save_to_db(PROCESSED_FOLDER, DB_PATH, TABLE_NAME)
