import os


def save_document(content, file_path):
    # Ensure the target directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the content into the file
    with open(file_path, 'w') as file:
        file.write(content)


def file_exists(file_path):
    # Check if the file exists at the given path
    return os.path.exists(file_path)


def filePathByURL(baseFolder, url):
    return os.path.join(baseFolder, url.split('//')[1].replace('/', '_')) + ".txt"
