import os
import pandas as pd
from datetime import datetime, timedelta
import logging
import re

def limpar_caracteres_especiais(texto):
    """Remove caracteres especiais de strings, exceto para colunas de data/hora."""
    if isinstance(texto, str):
        return re.sub(r"[^a-zA-Z0-9\s:/\-]", "", texto)  # Mantém letras, números, espaço, :, / e -
    return texto

def process_and_convert_to_excel(extract_dir="arquivos_extraidos", output_dir="dados_tratados"):
    """Processa arquivos CSV de todas as subpastas dentro da pasta extraída, convertendo UTC para Brasília e limpando os dados."""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logging.info(f"📂 Verificando arquivos dentro de subpastas em: {extract_dir}")

    arquivos_encontrados = False  # Para verificar se encontramos arquivos

    # Percorre todas as subpastas dentro de arquivos_extraidos
    for root, dirs, files in os.walk(extract_dir):
        # Debug: Verificando se estamos percorrendo a pasta certa
        logging.info(f"📂 Verificando a pasta: {root}")

        for file in files:
            # Verifica se o arquivo é CSV
            if file.endswith(".csv"):  # Confirma que é um arquivo CSV
                arquivos_encontrados = True
                file_path = os.path.join(root, file)  # Caminho completo do arquivo
                logging.info(f"✅ Arquivo encontrado: {file_path}")
                
                try:
                    # Carregando o CSV
                    df = pd.read_csv(file_path, encoding="latin1", sep=";", low_memory=False)
                    
                    # Verifica quantas colunas o arquivo tem
                    logging.info(f"🔍 {file} contém {len(df.columns)} colunas.")

                    # Renomeando as colunas (ajuste conforme necessário)
                    novo_nomes_colunas = [
                        "Data", "Hora_UTC", "Temp_Max", "Temp_Min", "Umidade", "Pressao",
                        "Vento_Dir", "Vento_Vel", "Precipitacao", "Radiação_Solar", "Ponto_Orvalho",
                        "Nevoa", "Nebulosidade", "Evaporacao", "Sol_Diario", "Indice_UV",
                        "Sensacao_Termica", "Nivel_Mar", "Rajada_Vento"
                    ]
                    
                    if len(df.columns) == 19:
                        df.columns = novo_nomes_colunas
                    else:
                        logging.warning(f"⚠️ {file} tem {len(df.columns)} colunas, esperado 19. Verifique a estrutura!")

                    # Convertendo hora UTC para horário de Brasília (UTC-3)
                    df["Hora_UTC"] = pd.to_datetime(df["Hora_UTC"], errors="coerce")
                    df["Hora_Brasilia"] = df["Hora_UTC"] - timedelta(hours=3)

                    # Aplicando limpeza nos dados (exceto na coluna de data/hora)
                    for col in df.columns:
                        if col not in ["Data", "Hora_UTC", "Hora_Brasilia"]:
                            df[col] = df[col].apply(limpar_caracteres_especiais)

                    # Criar subpasta correspondente no output_dir
                    subpasta = os.path.relpath(root, extract_dir)  # Ex: "2000", "2001"
                    output_subdir = os.path.join(output_dir, subpasta)
                    os.makedirs(output_subdir, exist_ok=True)

                    # Caminho de saída
                    output_file = os.path.join(output_subdir, file.replace(".csv", ".xlsx"))
                    df.to_excel(output_file, index=False)

                    logging.info(f"📁 Arquivo salvo em: {output_file}")
                
                except Exception as e:
                    logging.error(f"❌ Erro ao processar {file}: {e}")

    if not arquivos_encontrados:
        logging.error("🚨 Nenhum arquivo CSV encontrado dentro das subpastas!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    process_and_convert_to_excel()
