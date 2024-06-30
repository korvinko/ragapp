from langchain_community.document_loaders import DirectoryLoader
from helpers import getVectorStore

# Load documents
loader = DirectoryLoader("/home/korvinko/Documents/Datasets/zendit", glob="**/*")
docs = loader.load()
print(len(docs))

vc = getVectorStore()

# Save document embeddings to LanceDB
vc.add_documents(docs)
