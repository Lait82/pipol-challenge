from .article import Article
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging


class ArticleScraper:
    def __init__(self, driver: webdriver.Chrome ):
        self.driver = driver

    def get_articles(self) -> list[Article]:
        containers = self.driver.find_elements(By.XPATH, "//div[@slot and @data][.//div[@class='contenedor_dato_modulo '][div[@class='volanta_titulo']]]")
        articles = [Article(container) for container in containers]
        logging.info("Successfully scraped ", len(articles), " news.")
        return articles