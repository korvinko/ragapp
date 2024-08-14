
### Actions

create-dataset:
	python 1_load_websites_to_files.py

load-dataset:
	python 2_load_dataset.py

test-rag:
	python 3_optional_test_rag.py

start-server:
	uvicorn 4_rest_app:app --reload --host 0.0.0.0 --port 8000

### Infrastructure

docker-build:
	docker build -t ragapp -f docker/Dockerfile .

docker-test-run:
	docker run --rm ragapp

compose-build:
	docker compose -f docker/docker-compose.yml build

compose-start:
	docker compose -f docker/docker-compose.yml up

push-docker-images:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 117521322591.dkr.ecr.us-east-1.amazonaws.com

    docker tag docker-ragapp 117521322591.dkr.ecr.us-east-1.amazonaws.com/ai-assistant-rag
    docker push 117521322591.dkr.ecr.us-east-1.amazonaws.com/ai-assistant-rag

    docker tag ollama/ollama 117521322591.dkr.ecr.us-east-1.amazonaws.com/ai-assistant-ollama
    docker push 117521322591.dkr.ecr.us-east-1.amazonaws.com/ai-assistant-ollama