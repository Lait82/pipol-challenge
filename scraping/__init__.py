# from .Article import Article  # Importa y expone la clase al paquete
from .article_scraper import ArticleScraper
from .article import Article

__all__ = ['ArticleScraper', 'Article']  # Lista de lo que se exporta (opcional pero recomendado)