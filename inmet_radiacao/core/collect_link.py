import os
import requests
from bs4 import BeautifulSoup
from config import INPUT_FOLDER

URL_BASE = "https://portal.inmet.gov.br/dadoshistoricos"


def coletar_links():
    response = requests.get(URL_BASE)
    soup = BeautifulSoup(response.content, "html.parser")

    links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and href.endswith(".zip"):
            links.append(href)

    os.makedirs(INPUT_FOLDER, exist_ok=True)
    with open(os.path.join(INPUT_FOLDER, "links.txt"), "w") as f:
        for link in links:
            f.write(link + "\n")