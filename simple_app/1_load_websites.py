
from helpers import CustomWebBaseLoader, getVectorStore
from helpers import DatasetCleaner
from helpers import filterByHtmlTag
from helpers import getDoc
from langchain_community.document_loaders import AsyncChromiumLoader

docs = []
dc = DatasetCleaner()

urls = [
    "https://developers.zendit.io/zendit-university/",
    "https://developers.zendit.io/zendit-university/zendit-wallets/",
    "https://developers.zendit.io/zendit-university/zendit-catalog/",
    "https://developers.zendit.io/zendit-university/zendit-security/",
    "https://developers.zendit.io/zendit-university/zendit-test-mode/",
    "https://developers.zendit.io/zendit-university/transaction-processing/",
    "https://developers.zendit.io/zendit-university/webhooks/",
    "https://developers.zendit.io/zendit-university/queue-and-retry/",
    "https://developers.zendit.io/zendit-university/zendit-alerts/",
    "https://developers.zendit.io/zendit-university/zendit-shieldwall/",
    "https://developers.zendit.io/zendit-university/esims/",
    "https://developers.zendit.io/zendit-university/zendit-production-checklist/",
]

jsBasedUrls = [
    "https://developers.zendit.io/api/"
]

loader = AsyncChromiumLoader(jsBasedUrls, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'")
chromeDocs = loader.load()

css_class = "api-content"
for doc in chromeDocs:
    item = filterByHtmlTag(doc.metadata['source'], doc.page_content, css_class)
    result = dc.clean(str(item))
    finalDoc = getDoc(doc.metadata['source'], result)
    docs.append(finalDoc)

css_class = 'p-xl-5'
for url in urls:
    loader = CustomWebBaseLoader(url, css_class)
    content = loader.load()
    result = dc.clean(str(content))
    finalDoc = getDoc(url, result)
    docs.append(finalDoc)

vc = getVectorStore()

vc.add_documents(docs)
