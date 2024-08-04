import google.generativeai as genai
import os


class DatasetCleaner:
    def __init__(self):
        # Replace with your actual Gemini API key
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-pro')
        self.prompt = """Output content must not include replies from LLM, just content to save in a file. Please retain the original content as much as possible, clean up any non-text markup, and ensure the text is clear and readable. It must not include HTML tags or JavaScript code, only plain, logical text except for code which is part of the documentation. Save the http link to the original at the end.
        Text: """

    def clean(self, content: str):
        response = self.model.generate_content(self.prompt + content)
        return response.text
