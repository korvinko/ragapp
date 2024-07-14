# import
import requests
from langchain_community.vectorstores import LanceDB
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
import lancedb
from langchain_core.documents import Document
from bs4 import BeautifulSoup

from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

def getEmbeddings():
    # create the open-source embedding function
    return OllamaEmbeddings(base_url="http://localhost:11434", model="rjmalagon/gte-qwen2-7b-instruct-embed-f16")

def getVectorStore():
    # Connect to local LanceDB
    db_path = "/home/korvinko/Documents/store/zendit"  # Adjust the path as necessary for your setup
    db = lancedb.connect(uri=db_path)

    # create the open-source embedding function
    embeddings = getEmbeddings()

    # Initialize LanceDB vector store
    vc = LanceDB(
        uri=db_path,
        embedding=embeddings,
        table_name='zendit_university'
    )

    return vc

def filterByHtmlTag(url: str, body: str, cssClass: str):
        soup = BeautifulSoup(body, 'html.parser')
        elements = soup.find_all(class_=cssClass)
        content = '\n'.join(element.get_text() for element in elements)
        return content

def getDoc(url: str, content: str):
        doc = Document(page_content=content, metadata={"source": url})
        return doc

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

class DatasetCleaner:
    llm: Ollama
    prompt: str

    def __init__(self):
        self.llm = Ollama(
            model="qwen2:7b",
            num_ctx=25048, # input number of token limit
            num_predict=25048, # output number of token limit
            temperature=0.3, # precise
        )
        self.prompt = """Please clean up the following text by removing any non-text markup and ensuring the text is clear and readable. Retain the original content as much as possible. It must not include HTML tags or JavaScript code, only plain, logical text. Just return the content.
        Text: """

    def clean(self, content: str):
        response = self.llm.invoke(self.prompt + content)
        return response

