import os
import re
import json
import logging
from selenium.webdriver.remote.webelement import WebElement
import requests

def response_parser(response_text: str) -> list[dict]:
    """
    Extrae una lista de dicts desde una respuesta tipo string (como la que devuelve un LLM).
    """
    try:
        # Caso 1: string es un JSON limpio
        parsed = json.loads(response_text)
        if isinstance(parsed, dict):
            return [parsed]
        if isinstance(parsed, list):
            return parsed
    except json.JSONDecodeError:
        pass

    # Caso 2: extraer JSON dentro de texto con regex
    match = re.search(r'(\[\s*{.*?}\s*.*?\]|\{.*?\})', response_text, re.DOTALL)
    if match:
        try:
            parsed = json.loads(match.group(1))
            if isinstance(parsed, dict):
                return [parsed]
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError as e:
            logging.error("Error al parsear JSON embebido:", e)

    logging.warning("No se pudo parsear la respuesta como JSON.")
    return []


class DynamicArticleParser:
    def __init__(self, model="mistralai/Mistral-7B-Instruct-v0.2"):
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('HF_API_KEY')}",
            "Content-Type": "application/json"
        }

    def extract_info(self, html_element: WebElement):
        html = html_element.get_attribute('innerHTML')
        prompt = f"""
Extraé el título, kicker, link y URL de imagen de cada artículo del siguiente bloque HTML.
Enfocate exclusivamente en los artículos que tengan todos estos componentes.
No puede haber un artículo sin kicker.
Respondé un array de objetos en JSON con las claves: title, kicker, link, img_url.

HTML:
{html}
"""

        payload = {
            "inputs": prompt
        }
        logging.info("Llamando a Hugging Face API...")
        response = requests.post(self.api_url, headers=self.headers, json=payload)

        try:
            content = response.json()
            if isinstance(content, list) and 'generated_text' in content[0]:
                response_text = content[0]['generated_text']
            elif isinstance(content, dict) and 'generated_text' in content:
                response_text = content['generated_text']
            else:
                # fallback: todo el JSON
                response_text = json.dumps(content)

            return response_parser(response_text)

        except Exception as e:
            logging.error(f"Error procesando respuesta HuggingFace: {e}")
            return []