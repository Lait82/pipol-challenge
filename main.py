# Script
from dotenv import load_dotenv
import logging
import argparse


# Scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from scraping.article_scraper import ArticleScraper
from scraping.dynamic_article_parser import DynamicArticleParser


# Data processing
from data_processing.extract_metrics import extract_metrics_from_articles

# Clients
from clients.bigquery_client import get_client as get_bigquery_client
from clients.openai_client import get_client as get_openai_client

# Cloud
from loaders.bigquery_loader import load_df_to_bigquery

def set_up_driver() -> webdriver.Chrome:
    chrome_options = ChromeOptions() 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)


def main(ai_scraping: bool):
    # Basic setup.
    load_dotenv()
    my_url = 'https://www.yogonet.com/international/'    
    driver = set_up_driver()
    driver.get(my_url)
    scraper = ArticleScraper(driver)


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
    articles = None
    if(ai_scraping):
        # AI based analysis.
        openai_client = get_openai_client()
        parser = DynamicArticleParser(openai_client)
        articles = scraper.get_ia_scraped_articles(parser)
    
    else:
        articles = scraper.get_articles()
    

    # Process data.
    word_counts_df, \
    char_counts_df, \
    capitalized_words_df = extract_metrics_from_articles(articles)

    # Load the dta to bigquery.
    bigquery_client = get_bigquery_client()
    load_df_to_bigquery(bigquery_client, word_counts_df, 'word_frequency')
    load_df_to_bigquery(bigquery_client, char_counts_df, 'char_frequency')
    load_df_to_bigquery(bigquery_client, capitalized_words_df, 'capitalized_words')

    logging.info("Ejecución finalizada.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script that scrapes info from a news website and uploads some metrics of the info."
    )
    parser.add_argument("--ai-based-scraping", action="store_true", help="If set, enables AI-based scraping logic.")
    args = parser.parse_args()

    main(args.ai_based_scraping)