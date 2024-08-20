# Project Setup

Follow these steps to set up and run the project.

## Prepare local environment

### Configure environment variables

Create .env file in the root directory by copying the .env.localhost file:
```bash
cp .env_localhost .env 
```

Provide your own values in the .env file:
```env
BASE_FOLDER="/path/to/the/dataset/files"
DATABASE_PATH="/path/to/the/vectore/db/files"
DATABASE_TABLE="TABLE_NAME_OF_YOUR_DB"
```

### Install Ollama
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
```

### Pull models
```bash
ollama pull llama3.1:8b
ollama pull Losspost/stella_en_1.5b_v5
```

### Install Dependencies
Install all necessary dependencies using pip:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Create the Dataset
Create the dataset:
```bash
make create-dataset
```

## Load Dataset
Load the dataset to vector database:
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

## Prepare docker environment

### Configure environment variables

Create .env file in the root directory by copying the .env.docker file:
```bash
cp .env_docker .env 
```

### Build docker images
```bash
make compose-build
```

### Start docker images
```bash
make compose-start
```

### Test app
```bash
curl --location 'http://localhost:8001/ask' \
--header 'Content-Type: application/json' \
--data '{"query": "Tell me about security features"}'
```
