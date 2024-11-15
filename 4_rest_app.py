from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from libs.storage import get_vector_store
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import os
import random
import string
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Mount the static directory to serve HTML and other static files
app.mount("/web", StaticFiles(directory="./static"), name="index.html")

# Define request body
class QueryRequest(BaseModel):
    query: str
    historyKey: str

# Define the prompt template
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know; don't try to make up an answer. Be as concise as possible, but provide all details if the user asks.
{context}
Question: {question}. This question is related to the service zendit.io. Provide the URL to the documentation next to the provided information. Return output in markdown format.
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

# Set up the vector store and model
vc = get_vector_store()
# Initialize memory for conversation
llm = Ollama(model=os.getenv("OLLAMA_MAIN_MODEL"), base_url=os.getenv("OLLAMA_ADDRESS"), callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))

def generate_history_key(length=12):
    characters = string.ascii_letters + string.digits  # You can also add string.punctuation for special characters
    return ''.join(random.choice(characters) for _ in range(length))


randomString = generate_history_key()

@app.post("/ask")
def ask(query_request: QueryRequest):
    try:
        # In your function
        # logger.info(f"History Key: {historyKey}")

        memory = ConversationBufferMemory(memory_key=query_request.historyKey, return_messages=True)

        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vc.as_retriever(),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            memory=memory
        )

        result = qa_chain({"query": query_request.query})
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the app, use the following command in terminal
# uvicorn api:app --reload --host 0.0.0.0 --port 8000
