import os
from groq import Groq


class DatasetCleaner:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.prompt = """Output content must not include replies from LLM, just content to save in a file. Please retain the original content as much as possible, clean up any non-text markup, and ensure the text is clear and readable. It must not include HTML tags or JavaScript code, only plain, logical text except for code which is part of the documentation. Save the http link to the original at the end.
        Text: """

    def clean(self, content: str):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": self.prompt + content,
                }
            ],
            model="llama3-70b-8192",
        )
        return chat_completion.choices[0].message.content
