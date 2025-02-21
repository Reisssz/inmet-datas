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
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
            driver.get("https://portal.inmet.gov.br/dadoshistoricos")

            # Obtendo e processando o código-fonte da página diretamente
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extraindo links dos arquivos ZIP
            links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".zip")]

            logger.info(f"Links encontrados: {links}")
            return links

    except Exception as e:
        logger.error(f"Erro ao coletar links: {e}")
        return []
