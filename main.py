# Script
from dotenv import load_dotenv
import logging
import argparse
import os


# Scraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from scraping.article_scraper import ArticleScraper
from scraping.dynamic_article_parser import DynamicArticleParser


# Data processing
from data_processing.extract_metrics import extract_metrics_from_articles

# Clients
from clients.bigquery_client import get_client as get_bigquery_client

# Cloud
from loaders.bigquery_loader import load_df_to_bigquery

def set_up_driver() -> webdriver.Chrome:
    chrome_options = ChromeOptions() 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)



def main(ai_scraping: bool = False):
    # Basic setup.
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
        parser = DynamicArticleParser()
        articles = scraper.get_ia_scraped_articles(parser)
    
    else:
        articles = scraper.get_articles()
    
    # Process data.
    word_counts_df, \
    char_counts_df, \
    capitalized_words_df = extract_metrics_from_articles(articles)

    # Load the dta to bigquery.
    bigquery_client = get_bigquery_client()

    # Since AI scraping may fail, only uploads data if theres any.
    if(ai_scraping):
        if(len(word_counts_df)):
            load_df_to_bigquery(bigquery_client, word_counts_df, 'word_frequency')
        if(len(capitalized_words_df)):
            load_df_to_bigquery(bigquery_client, capitalized_words_df, 'capitalized_words')
        if(len(char_counts_df)):
            load_df_to_bigquery(bigquery_client, char_counts_df, 'char_frequency')
    load_df_to_bigquery(bigquery_client, word_counts_df, 'word_frequency')
    load_df_to_bigquery(bigquery_client, capitalized_words_df, 'capitalized_words')
    load_df_to_bigquery(bigquery_client, char_counts_df, 'char_frequency')
    
    

    logging.info("Ejecución finalizada.")

def deps_checker() -> bool:
    # Check de archivos
    env_files = [
        "./.env",
        "./credentials.json"
        ]
    for file_path in env_files:
        if not(os.path.exists(file_path)) or os.path.getsize(file_path) <= 0:
            logging.fatal(f"The file '{var}' is missing or it's empty.")
            exit()

    # Vars needed
    env_vars = [
        'GOOGLE_APPLICATION_CREDENTIALS',
        'GOOGLE_PROJECT_ID',
        'BIGQUERY_DATASET',
        'HF_API_KEY'
    ]

    for var in env_vars:
        if os.getenv(var) == None:
            logging.fatal(f"The variable '{var}' in the .env file is not set.")
            exit()
    

if __name__ == "__main__":
    # Args
    parser = argparse.ArgumentParser(
        description="Script that scrapes info from a news website and uploads some metrics of the info."
    )
    parser.add_argument("--local", action="store_true", help="If set, enables cli features and testing. If not set, the script assumes everything is setted properly.")
    parser.add_argument("--ai-based-scraping", action="store_true", help="If set, enables AI-based scraping logic.")
    args = parser.parse_args()

    if(args.local):
        # Deps checker
        load_dotenv()
        deps_checker()
    
    # CLI override
    if args.ai_based_scraping:
        ai_scraping = True
    else:
        # Env fallback
        ai_scraping = os.getenv("AI_BASED_SCRAPING", "false").lower() == "true"

    main(ai_scraping)