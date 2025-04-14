from .article import Article
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from .dto.article import ArticleDTO
from .dynamic_article_parser import DynamicArticleParser


class ArticleScraper:
    def __init__(self, driver: webdriver.Chrome ):
        self.driver = driver

    def get_articles(self) -> list[ArticleDTO]:
        containers = self.driver.find_elements(By.XPATH, "//div[@slot and @data][.//div[@class='contenedor_dato_modulo '][div[@class='volanta_titulo']]]")
        articles = [Article(container) for container in containers]
        logging.info("Successfully scraped {0} news.".format(len(articles)))
        return articles
    
    def get_ia_scraped_articles(self, parser: DynamicArticleParser) -> list[ArticleDTO]:
        """Si falla la api devuelve toda la data procesada hasta el momento"""
        candidates = self.driver.find_elements(By.XPATH, "//div[@slot and @data]")

        articles:list[ArticleDTO] = []
        for candidate in candidates:
            info = parser.extract_info(candidate)
            try:
                articles.extend([ArticleDTO.from_dict(item) for item in info])
            except ValueError as e:
                logging.error(e)
                if(len(articles)):
                    return articles

        return articles