# Scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Basic
from dotenv import load_dotenv
import logging
import re
import os

# Data
import pandas as pd
from collections import Counter
from classes.article_scraper import ArticleScraper

# Cloud
from clients.bigquery_client import get_client as get_bigquery_client
from google.cloud import bigquery

def set_up_driver() -> webdriver.Chrome:
    chrome_options = ChromeOptions() 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)


def main():

    # Basic setup
    load_dotenv()
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


    ##### CLOUD
    word_counts_df = word_counts.reset_index().rename(columns={"index": "word", 0: "count"})
    char_counts_df = word_counts.reset_index().rename(columns={"index": "character", 0: "count"})
    capitalized_words_df = pd.DataFrame(unique_capitalized, columns=["word"])

    # input("halting")
    # Nombre completo de la tabla
    project_name = os.getenv("BIGQUERY_PROJECT_NAME")
    dataset = os.getenv("BIGQUERY_DATASET")

    # Configuración del job de carga y client
    bigquery_client = get_bigquery_client()
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
    )

    # Ejecutar el job
    job = bigquery_client.load_table_from_dataframe(word_counts_df, '.'.join((project_name, dataset, "word_frequency")), job_config=job_config)
    job = bigquery_client.load_table_from_dataframe(char_counts_df, '.'.join((project_name, dataset, "char_frequency")), job_config=job_config)
    job = bigquery_client.load_table_from_dataframe(capitalized_words_df, '.'.join((project_name, dataset, "capitalized_words")), job_config=job_config)


    # Esperar a que termine (bloqueante)
    job.result()

    logging.info("Tablas subidas")

if __name__ == "__main__":
    main()