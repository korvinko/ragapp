import os

from langchain_ollama.llms import OllamaLLM


class DatasetCleaner:
    llm: OllamaLLM
    prompt: str

    def __init__(self):
        self.llm = OllamaLLM(
            model=os.getenv("OLLAMA_MAIN_MODEL"),
            num_ctx=25048,  # input number of token limit
            num_predict=25048,  # output number of token limit
            temperature=0.3,  # precise
        )
        self.prompt = """Output content must not include replies from LLM, just content to save in a file. Please retain the original content as much as possible, clean up any non-text markup, and ensure the text is clear and readable. It must not include HTML tags or JavaScript code, only plain, logical text except for code which is part of the documentation. Save the http link to the original at the end.
        Text: """

    def clean(self, content: str):
        response = self.llm.invoke(self.prompt + content)
        return response
