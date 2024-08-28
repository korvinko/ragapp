from fastapi import HTTPException
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import markdown
from libs.storage import get_vector_store
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import random
import string
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update as necessary for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
llm = Ollama(
    model=os.getenv("OLLAMA_MAIN_MODEL"),
    base_url=os.getenv("OLLAMA_ADDRESS"),
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    temperature=0.1,
)

def generate_history_key(length=12):
    characters = string.ascii_letters + string.digits  # You can also add string.punctuation for special characters
    return ''.join(random.choice(characters) for _ in range(length))

@app.post("/ask")
def ask(query_request: QueryRequest):
    try:
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


# Define a message format for conversation
class Message(BaseModel):
    role: str  # 'system', 'user', or 'assistant'
    content: str

# Define request body
class QueryRequestV2(BaseModel):
    query: List[Message]  # Expect a list of messages
    historyKey: str = ""

@app.post("/completion")
async def completions(request: Request):
    try:
        body_json = await request.json()
        prompt = body_json.get("prompt")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str("Error parsing JSON body:" + str(e)))

    try:
        qa_chain = RetrievalQA.from_chain_type(
            llm,
            retriever=vc.as_retriever(),
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
            chain_type="stuff",
        )

        result = qa_chain({"query": prompt})
        resp = result.get("result")

        # Convert Markdown to HTML
        html_resp = markdown.markdown(
            resp,
            extensions=["extra", "sane_lists"]  # Better Markdown list and formatting handling
        )

        # Convert Markdown to HTML
        html_resp = markdown.markdown(resp)

        return HTMLResponse(content=html_resp, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the app, use the following command in terminal
# uvicorn api:app --reload --host 0.0.0.0 --port 8000