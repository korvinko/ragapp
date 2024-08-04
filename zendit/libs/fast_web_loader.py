import requests
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from bs4 import BeautifulSoup


class CustomWebBaseLoader(WebBaseLoader):
    def __init__(self, url: str, css_class: str):
        self.url = url
        self.css_class = css_class

    def load(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(class_=self.css_class)
        content = '\n'.join(element.get_text() for element in elements)
        doc = Document(page_content=content, metadata={"source": self.url})
        return doc
