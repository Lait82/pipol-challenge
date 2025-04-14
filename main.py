# Scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Basic
from dotenv import load_dotenv
import logging
import re
import os

# Data
from scraping.article_scraper import ArticleScraper
from data_processing.extract_metrics import extract_metrics_from_articles

# Cloud
from clients.bigquery_client import get_client as get_bigquery_client
from google.cloud import bigquery
from loaders.bigquery_loader import load_df_to_bigquery

def set_up_driver() -> webdriver.Chrome:
    chrome_options = ChromeOptions() 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)


def main():
    # Basic setup.
    load_dotenv()
    my_url = 'https://www.yogonet.com/international/'    
    driver = set_up_driver()
    driver.get(my_url)


    # Logger setup.
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler("script.log"),
            logging.StreamHandler()
        ]
    )
    
    # Scrape the site.
    scraper = ArticleScraper(driver)
    articles = scraper.get_articles()

    # Process data.
    word_counts_df, \
    char_counts_df, \
    capitalized_words_df = extract_metrics_from_articles(articles)

    # Load the dta to bigquery.
    bigquery_client = get_bigquery_client()
    load_df_to_bigquery(bigquery_client, word_counts_df, 'word_frequency')
    load_df_to_bigquery(bigquery_client, char_counts_df, 'char_frequency')
    load_df_to_bigquery(capitalized_words_df, word_counts_df, 'capitalized_words')

if __name__ == "__main__":
    main()