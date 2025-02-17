import pandas as pd
from datetime import timedelta
import re
import logging

def processar_dados(file_path):
    """Processa um arquivo CSV, convertendo UTC para Brasília e limpando os dados."""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Carregando o CSV
        df = pd.read_csv(file_path, encoding="latin1", sep=";", low_memory=False)
        
        # Renomeando as colunas
        novo_nomes_colunas = [
            "Data", "Hora_UTC", "Temp_Max", "Temp_Min", "Umidade", "Pressao",
            "Vento_Dir", "Vento_Vel", "Precipitacao", "Radiação_Solar", "Ponto_Orvalho",
            "Nevoa", "Nebulosidade", "Evaporacao", "Sol_Diario", "Indice_UV",
            "Sensacao_Termica", "Nivel_Mar", "Rajada_Vento"
        ]
        
        if len(df.columns) == 19:
            df.columns = novo_nomes_colunas
        else:
            logger.warning(f"⚠️ {file_path} tem {len(df.columns)} colunas, esperado 19. Verifique a estrutura!")

        # Convertendo hora UTC para horário de Brasília (UTC-3)
        df["Hora_UTC"] = pd.to_datetime(df["Hora_UTC"], errors="coerce")
        df["Hora_Brasilia"] = df["Hora_UTC"] - timedelta(hours=3)

        # Aplicando limpeza nos dados (exceto nas colunas de data/hora)
        for col in df.columns:
            if col not in ["Data", "Hora_UTC", "Hora_Brasilia"]:
                df[col] = df[col].apply(lambda x: re.sub(r"[^a-zA-Z0-9\s:/\-]", "", str(x)))  # Limpeza de caracteres especiais

        # Salvando como Excel
        output_file = file_path.replace(".csv", ".xlsx")
        df.to_excel(output_file, index=False)

        logger.info(f"📁 Arquivo salvo em: {output_file}")
    
    except Exception as e:
        logger.error(f"❌ Erro ao processar {file_path}: {e}")