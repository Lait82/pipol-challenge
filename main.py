from selenium import webdriver
import os
import requests

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from .classes import Article

from time import sleep
import pandas as pd

def set_up_driver() -> webdriver.Chrome:
    chrome_options = ChromeOptions() 
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=chrome_options)


def main():
    my_url = 'https://www.yogonet.com/international/'
    
    driver = set_up_driver()
    driver.get(my_url)

    # Querying la web para obtener todos los articulos
    # articles = driver.find_elements(By.XPATH, "//div[@slot='news' and @id='main-container']//div[contains(@class, 'article-item')]")
    articles = driver.find_elements(By.XPATH, "//div[@slot and @data]//div[contains(@class, 'contenedor-dato-modulo')]")
    # full_header = driver.find_element(By.XPATH, "/html/body/div[4]/div[6]/div/div[1]/div") # Mejorar query
    # header_text = full_header.find_element(By.XPATH, "./div")
    

    # Datos 
    kicker_elem = header_text.find_element(By.XPATH, "div")
    title_elem = header_text.find_element(By.XPATH, "h2/a")
    link = title_elem.get_attribute("href")

    word_count_title = len(title_elem.text.split(' '))
    char_count_title = len([char for char in title_elem.text]) # Inclusive los whitespaces
    capitalized_words_title = len([ word for word in title_elem.text.split(' ') if word[0].isupper()])

    payload = {
        "word_count_title": word_count_title, 
        "char_count_title": char_count_title, 
        "capitalized_words_title": capitalized_words_title}
    print(payload)
    # print(kicker.text)



if __name__ == "__main__":
    main()