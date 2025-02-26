import sqlite3
import pandas as pd
import os

# Caminho do arquivo CSV (ajustado para o arquivo correto dentro da pasta)
caminho_arquivo_csv = os.path.join(os.path.dirname(__file__), "data", "arquivos_processados", "INMET_CO_DF_A046_GAMA (PONTE ALTA)_01-01-2025_A_31-01-2025.CSV")

# Nome do banco de dados SQLite
banco_de_dados = 'dados.db'

# Carregar o CSV em um DataFrame do Pandas
df = pd.read_csv(caminho_arquivo_csv, sep=";", encoding="latin-1")

# Conectar ao banco de dados SQLite (o arquivo será criado se não existir)
conn = sqlite3.connect(banco_de_dados)
cursor = conn.cursor()

# Criar a tabela no banco de dados com base nas colunas do DataFrame
colunas = ", ".join([f'"{coluna.replace(" ", "_")}" TEXT' for coluna in df.columns])  # Substitui espaços por _ em nomes de colunas

# Criar a consulta de criação da tabela
create_table_query = f"""
CREATE TABLE IF NOT EXISTS dados_processados (
    {colunas}
);
"""

# Tenta executar a consulta
try:
    cursor.execute(create_table_query)
except sqlite3.OperationalError as e:
    print(f"Erro na criação da tabela: {e}")
    print(f"Consulta SQL gerada: {create_table_query}")
    raise

# Inserir ou atualizar os dados do DataFrame no banco de dados
for index, row in df.iterrows():
    # Criação dinâmica do comando de inserção baseado nas colunas
    # Aqui assumimos que "DATA_HORA" seja um campo único, você pode alterar isso conforme necessário
    data_hora = row['DATA_HORA']
    
    # Verifique se já existe um registro com a mesma data_hora
    check_query = f'SELECT COUNT(*) FROM dados_processados WHERE "DATA_HORA" = ?'
    cursor.execute(check_query, (data_hora,))
    count = cursor.fetchone()[0]

    if count > 0:
        # Atualizar dados existentes se necessário
        update_query = f"""
        UPDATE dados_processados 
        SET 
            "PRECIP_TOTAL" = ?, 
            "PRESSAO_ATM" = ?, 
            "PRESSAO_MAX" = ?, 
            "PRESSAO_MIN" = ?, 
            "RADIACAO" = ?, 
            "TEMP_AR" = ?, 
            "TEMP_ORVALHO" = ?, 
            "TEMP_MAX" = ?, 
            "TEMP_MIN" = ?, 
            "TEMP_ORV_MAX" = ?, 
            "TEMP_ORV_MIN" = ?, 
            "UMID_MAX" = ?, 
            "UMID_MIN" = ?, 
            "UMID_AR" = ?, 
            "VENTO_DIR" = ?, 
            "VENTO_RAJADA" = ?, 
            "VENTO_VEL" = ?, 
            "REGIÃO" = ?, 
            "UF" = ?, 
            "ESTAÇÃO" = ?, 
            "CODIGO__WMO_" = ?, 
            "LATITUDE" = ?, 
            "LONGITUDE" = ?, 
            "ALTITUDE" = ?, 
            "DATA_DE_FUNDAÇÃO__YYYY-MM-DD_" = ?
        WHERE "DATA_HORA" = ?
        """
        cursor.execute(update_query, tuple(row) + (data_hora,))
    else:
        # Inserir dados novos
        insert_query = f"""
        INSERT INTO dados_processados ({', '.join([f'"{col}"' for col in df.columns])})
        VALUES ({', '.join(['?' for _ in df.columns])})
        """
        cursor.execute(insert_query, tuple(row))

# Commit para salvar as mudanças no banco
conn.commit()

# Fechar a conexão
conn.close()

print("Dados importados ou atualizados no banco de dados SQLite com sucesso!")
