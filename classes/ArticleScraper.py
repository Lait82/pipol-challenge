from .Article import Article
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class ArticleScraper:
    def __init__(self, driver: webdriver.Chrome ):
        self.driver = driver

    def get_articles(self) -> list[Article]:
        containers = self.driver.find_elements(By.XPATH, "//div[@slot and @data][.//div[@class='contenedor_dato_modulo '][div[@class='volanta_titulo']]]")
        return [Article(container) for container in containers]