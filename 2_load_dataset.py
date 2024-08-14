import os
from libs.storage import get_vector_store, load_docs, cleanup_vector_store
from dotenv import load_dotenv

load_dotenv()

dataset_folder = os.getenv("BASE_FOLDER")

docs = load_docs(dataset_folder)
cleanup_vector_store()
vs = get_vector_store()
vs.add_documents(docs)
