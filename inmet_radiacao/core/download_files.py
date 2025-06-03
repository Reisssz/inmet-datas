import os
import requests
from tqdm import tqdm
from config import INPUT_FOLDER


def baixar_arquivos():
    with open(os.path.join(INPUT_FOLDER, "links.txt"), "r") as f:
        links = [l.strip() for l in f.readlines()]

    for url in tqdm(links):
        nome = url.split("/")[-1]
        caminho = os.path.join(INPUT_FOLDER, nome)
        if os.path.exists(caminho):
            continue

        r = requests.get(url, stream=True)
        with open(caminho, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
