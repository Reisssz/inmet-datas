import os
import re
import pandas as pd
from core.treatment_files import extract_metadata, load_weather_data, save_to_csv
from config import EXTRACT_FOLDER, OUTPUT_FOLDER


def save_file():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    files = [
        f for f in os.listdir(EXTRACT_FOLDER)
        if re.match(r'INMET_.*\.CSV', f, re.IGNORECASE)
    ]

    print(f"🔍 {len(files)} arquivos encontrados na pasta de extração.")

    for file in files:
        input_path = os.path.join(EXTRACT_FOLDER, file)
        output_path = os.path.join(OUTPUT_FOLDER, file)

        if os.path.exists(output_path):
            print(f"✅ Já processado: {file}")
            continue

        meta = extract_metadata(input_path)
        if meta.empty:
            print(f"⚠️ Metadados ausentes: {file}")
            continue

        df = load_weather_data(input_path, meta)
        if df.empty:
            print(f"⚠️ Sem dados válidos: {file}")
            continue

        save_to_csv(df, output_path)
        print(f"📁 Arquivo salvo: {output_path}")

    print("✅ Processamento finalizado.")
