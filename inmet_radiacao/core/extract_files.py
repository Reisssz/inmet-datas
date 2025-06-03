import os
import zipfile
from config import INPUT_FOLDER, EXTRACT_FOLDER


def unzip_files():
    os.makedirs(EXTRACT_FOLDER, exist_ok=True)
    for file in os.listdir(INPUT_FOLDER):
        if file.endswith(".zip"):
            zip_path = os.path.join(INPUT_FOLDER, file)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(EXTRACT_FOLDER)