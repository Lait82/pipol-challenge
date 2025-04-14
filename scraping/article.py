from selenium.webdriver.remote.webelement import WebElement
import os
import requests
from selenium.webdriver.common.by import By
import logging
from .dto.article import ArticleDTO



class Article:
    def __init__(self, article: WebElement):
        # private
        self._article = article
        self.kicker = self._get_kicker_text()
        self.title = self._get_title_text()
        self.link = self._get_link()
        self.img_url = self._get_img_url()


    def _get_kicker_text(self) -> str | None:
        try:
            kicker_element = self._article.find_element(By.XPATH, "./div[1]/div[1]")
        except Exception:
            logging.warning("Kicker not found.")
            return None
        return kicker_element.text
    

    def _get_title_text(self) -> str | None:
        try:
            title_element = self._article.find_element(By.XPATH, ".//h2")
        except Exception: 
            logging.warning("Title not found.")
            return None
        return title_element.text


    def _get_link(self) -> str:
        try:
            link_element = self._article.find_element(By.XPATH, ".//a")
        except Exception:
            logging.warning("Link not found.")
        return link_element.get_attribute('href')
    
    
    def _get_img_url(self) -> str:
        try:
            img_element = self._article.find_element(By.XPATH, ".//img")
        except Exception: 
            logging.warning("Image not found.")
        return img_element.get_attribute('src')
    


    ######### PUBLIC METHODS #########
    # En el challenge decia que habia que scrapear la imagen, pero lei que bigquery no esta pensado para subir binarios
    # asi que dejo la funcion aca pero no creo que sea necesaria
    def download_image(self, img_url: str):
        img_name = img_url.split("/")[-1]
        img_path = os.path.join('.', img_name)
        response = requests.get(img_url, stream=True)
        with open(img_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Image downloaded successfully")

    def to_dto(self) -> ArticleDTO:
        return ArticleDTO(
            title=self.title,
            kicker=self.kicker,
            link=self.link,
            img_url=self.img_url
        )

    
