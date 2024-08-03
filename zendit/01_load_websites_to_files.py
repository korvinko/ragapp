from libs.web_loader import load_and_filter_content
from libs.cleaner_gemini import DatasetCleaner
from libs.files import save_document
from libs.files import filePathByURL
from libs.files import file_exists

urls_css_classes = [
    ("https://developers.zendit.io/zendit-university/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/zendit-wallets/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/zendit-catalog/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/zendit-security/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/zendit-test-mode/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/transaction-processing/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/webhooks/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/queue-and-retry/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/zendit-alerts/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/zendit-shieldwall/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/esims/", "p-xl-5"),
    ("https://developers.zendit.io/zendit-university/zendit-production-checklist/", "p-xl-5"),
    ("https://developers.zendit.io/api/", "api-content")
]

baseFolder = "/home/korvinko/Documents/Datasets/zendit_3"

dc = DatasetCleaner()

for url, css_class in urls_css_classes:
    file_path = filePathByURL(baseFolder, url)
    if file_exists(file_path):
        continue
    doc = load_and_filter_content(url, css_class)
    cleanDoc = dc.clean(doc)
    save_document(cleanDoc, file_path)