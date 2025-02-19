import os
import pandas as pd
import numpy as np

def load_metadata():
    # Criando os metadados manualmente
    meta_data = pd.DataFrame({
        "Chave": ["REGIÃO", "UF", "ESTAÇÃO", "CODIGO (WMO)", "LATITUDE", "LONGITUDE", "ALTITUDE", "DATA DE FUNDAÇÃO (YYYY-MM-DD)"],
        "Valor": ["CO", "GO", "GOIANIA", "A002", -16.64277777, -49.21999999, 770, "2001-05-29"]
    })
    
    # Definindo a chave como índice
    meta_data = meta_data.set_index("Chave").T
    
    return meta_data

def load_weather_data(file_path, meta_data):
    try:
        main_data = pd.read_csv(
            file_path,
            sep=";",
            encoding="latin-1",
            decimal=",",
            skiprows=8
        )

        names_columns = [
            "DATA", "HORA", "PRECIP_TOTAL", "PRESSAO_ATM", 
            "PRESSAO_MAX", "PRESSAO_MIN", "RADIACAO", 
            "TEMP_AR", "TEMP_ORVALHO", "TEMP_MAX", 
            "TEMP_MIN", "TEMP_ORV_MAX", "TEMP_ORV_MIN", 
            "UMID_MAX", "UMID_MIN", "UMID_AR", 
            "VENTO_DIR", "VENTO_RAJADA", "VENTO_VEL", 
            "UNNAMED"
        ]

        main_data.columns = names_columns
        main_data.replace(-9999, np.nan, inplace=True)

        # Ajuste na conversão da data para tratar o formato "YYYY/MM/DD HHMM UTC"
        main_data["DATA_HORA"] = pd.to_datetime(main_data["DATA"] + " " + main_data["HORA"], format="%Y/%m/%d %H%M UTC", errors='coerce')

        main_data = main_data.drop(columns=["DATA", "HORA", "UNNAMED"], errors='ignore')
        main_data = main_data[["DATA_HORA"] + [col for col in main_data.columns if col != "DATA_HORA"]]

        for column in meta_data.columns:
            main_data[column] = meta_data[column].iloc[0]

        return main_data 

    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

