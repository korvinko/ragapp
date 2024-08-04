# Project Setup

Follow these steps to set up and run the project.

## Prepare Environment

### Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
```

### Install Dependencies
Install all necessary dependencies using pip:
```bash
pip install
```

## Prepare the Dataset
Create the dataset:
```bash
make create-dataset
```

## Load Dataset
Load the dataset:
```bash
make load-dataset
```

## Test RAG
Run the tests for RAG (Retrieval-Augmented Generation):
```bash
make test-rag
```

## Start REST Server
Start the REST server:
```bash
make start-server
```