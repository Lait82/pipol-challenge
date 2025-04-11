from selenium.webdriver.remote.webelement import WebElement
import os
import requests

class Article:
    def __init__(self, article: WebElement):
        self._article = article
        self.kicker = ""
        self.title = ""
        self.link = ""
        self.img_url = ""
    
    ######### PRIVATE METHODS ########
    def _get_kicker_element(self) -> WebElement:
        pass
        # return self._article
    def _get_title_element(self) -> WebElement:
        pass
        # return WebElement



    ######### PUBLIC METHODS #########
    # En el challenge decia que habia que scrapear la imagen, pero lei que bigquery no esta pensado para subir binarios
    # asi que solo la descargo.
    def download_image(self, img_url: str):
        img_name = img_url.split("/")[-1]
        img_path = os.path.join('.', img_name)
        response = requests.get(img_url, stream=True)
        with open(img_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Image downloaded successfully")
    
    def get_kicker_text(self) -> str:
        kicker_element = self._get_kicker_element()
        pass
        # return str
    def get_title_text(self) -> str:
        pass
        # return str
    def get_link(self) -> str:
        pass
        # return str
    def get_img_url(self) -> str:
        pass
        # return str

# Might be useful later 
    # Descarga de la imagen
    # header_image = full_header.find_element(By.XPATH, ".//img")
    # img_url = header_image.get_attribute("src")
    # download_image(img_url)
# 