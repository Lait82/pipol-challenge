from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from classes.article_scraper import ArticleScraper

from collections import Counter
import pandas as pd
import logging
import re

def set_up_driver() -> webdriver.Chrome:
    chrome_options = ChromeOptions() 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)


def main():

    # Driver setup
    my_url = 'https://www.yogonet.com/international/'    
    driver = set_up_driver()
    driver.get(my_url)


    # Logger setup
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler("script.log"),
            logging.StreamHandler()
        ]
    )
    
    # Scrape the site
    scraper = ArticleScraper(driver)
    articles = scraper.get_articles()

    # Data processing 
    capitalized_words = []

    word_counter = Counter({})
    char_counter = Counter({})

    for a in articles:
        title = a.title
        if title is None:
            continue

        # Contar caracteres normalizados (lower, sin puntuación)
        clean_chars = list(title)
        char_counter.update(clean_chars)

        # Separar palabras normalizadas y contar
        words = re.findall(r'\b\w+\b', title.lower())
        word_counter.update(words)

        # Palabras capitalizadas tal como están en el título
        capitalized_words.extend(
            [w for w in title.split() if w.istitle()]
        )

    # Convertimos a pandas Series
    word_counts = pd.Series(word_counter).sort_values(ascending=False)
    char_counts = pd.Series(char_counter).sort_values(ascending=False)

    # Lista única de capitalizadas si querés
    unique_capitalized = list(set(capitalized_words))

    print("Palabras más comunes:")
    print(word_counts.head(1))
    print("Caracteres más comunes:")
    print(char_counts.head(10))
    print("Palabras capitalizadas:", unique_capitalized)


if __name__ == "__main__":
    main()