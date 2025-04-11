from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from classes.ArticleScraper import ArticleScraper

from time import sleep
import pandas as pd

def set_up_driver() -> webdriver.Chrome:
    chrome_options = ChromeOptions() 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)


def main():
    my_url = 'https://www.yogonet.com/international/'
    
    driver = set_up_driver()
    driver.get(my_url)

    # Querying la web para obtener todos los articulos
    scraper = ArticleScraper(driver)

    articles = scraper.get_articles()

    # Datos 
    # TODO: agregar try catch en todos los getters de article.
    # procesar los datos con pandas. 


if __name__ == "__main__":
    main()