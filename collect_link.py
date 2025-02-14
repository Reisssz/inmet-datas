from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def collect_links():
    """Coleta os arquivos ZIP do site e salva na pasta 'arquivos'."""

    # Configuração do ChromeOptions para abrir o navegador de forma invisível
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executa o Chrome sem abrir a janela
    options.add_argument("--disable-gpu")  # Evita problemas gráficos no Windows
    options.add_argument("--no-sandbox")  # Necessário para execução em alguns sistemas Linux
    options.add_argument("--disable-dev-shm-usage")  # Evita problemas de memória compartilhada

    # Inicializando o WebDriver com as opções headless
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get("https://portal.inmet.gov.br/dadoshistoricos")

    # Obtendo o código-fonte da página
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Extraindo links dos artigos
    articles = soup.find_all("article", class_="post-preview")
    links = [a["href"] for article in articles for a in article.find_all("a", href=True)]
    
    print("Links encontrados:", links)

    driver.quit()  # Fechando o navegador

    return links  # Retorna os links coletados
