from langchain_community.document_loaders import AsyncChromiumLoader
from bs4 import BeautifulSoup


def load_and_filter_content(url, selector):
    # Initialize AsyncChromiumLoader with the URL and a user agent
    loader = AsyncChromiumLoader([url],
                                 user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Load the document
    chromeDocs = loader.load()

    # Filter content by selector
    if chromeDocs:
        doc = chromeDocs[0]  # Assuming one document per URL
        filtered_content = filter_by_html_tag(doc.metadata['source'], doc.page_content, selector)
        return f"{filtered_content}\n\nSource URL: {doc.metadata['source']}"
    else:
        return f"Failed to load content from {url}"


def filter_by_html_tag(url: str, body: str, css_class: str):
    soup = BeautifulSoup(body, 'html.parser')
    elements = soup.find_all(class_=css_class)
    content = '\n'.join(element.get_text() for element in elements)
    return content
