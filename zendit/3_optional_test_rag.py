from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from libs.storage import get_vector_store
from dotenv import load_dotenv
import os

load_dotenv()

# Predefined query
query = "Tell me about security features. Provide all information."

# Prompt
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know; don't try to make up an answer. Be as concise as possible, but provide all details if the user asks.
{context}
Question: {question}. This question is related to the service zendit.io. Provide the URL to the documentation next to the provided information. Return output in markdown format.
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

vs = get_vector_store()

llm = Ollama(model=os.getenv("OLLAMA_MODEL"), callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]))
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vs.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
)

result = qa_chain({"query": query})

print(result)
