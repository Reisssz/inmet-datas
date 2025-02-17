from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import logging

def collect_links():
    """Coleta os arquivos ZIP do site e retorna uma lista de links."""
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Configuração do ChromeOptions para abrir o navegador de forma invisível
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Inicializando o WebDriver com as opções headless
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        driver.get("https://portal.inmet.gov.br/dadoshistoricos")

        # Obtendo o código-fonte da página
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Extraindo links dos arquivos ZIP
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.endswith(".zip"):
                links.append(href)

        logger.info(f"Links encontrados: {links}")

        driver.quit()  # Fechando o navegador

        return links  # Retorna os links coletados

    except Exception as e:
        logger.error(f"Erro ao coletar links: {e}")
        return []