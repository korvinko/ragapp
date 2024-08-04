from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from libs.storage import get_vector_store
import os

# Initialize FastAPI app
app = FastAPI()

# Define request body
class QueryRequest(BaseModel):
    query: str

# Define the prompt template
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible. Always answer in Zendit context. Return output in markdown format.  
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

# Set up the vector store and model
vc = get_vector_store()
llm = Ollama(model=os.getenv("OLLAMA_MODEL"), callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vc.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
)

@app.post("/ask")
def ask(query_request: QueryRequest):
    try:
        result = qa_chain({"query": query_request.query})
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the app, use the following command in terminal
# uvicorn api:app --reload --host 0.0.0.0 --port 8000
