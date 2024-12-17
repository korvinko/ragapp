from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import time

load_dotenv()

# Predefined query
query = "Tell me about security features. Provide all information."

# Prompt template
template = """Use the following information to answer the question below. If you don't know the answer, just say that you don't know; don't try to make up an answer. Be as concise as possible, but provide all details if the user asks.
Question: {question}. This question is related to the service zendit.io. Provide the URL to the documentation next to the provided information. Return output in markdown format.
Helpful Answer:"""
QA_PROMPT = PromptTemplate(
    input_variables=["question"],
    template=template,
)

# Initialize the language model
llm = OllamaLLM(
    model=os.getenv("OLLAMA_MAIN_MODEL"),
    base_url=os.getenv("OLLAMA_ADDRESS"),
    temperature=0.1,
)

# Format the prompt with the query
formatted_prompt = QA_PROMPT.format(question=query)

# Get the result from the model using streaming
stream = llm.stream(formatted_prompt)


start_time = time.time()
# Process the stream and print the output
for chunk in stream:
    print(chunk, end="", flush=True)

end_time = time.time()
print(f"\n\nProcessing time: {end_time - start_time:.2f} seconds")