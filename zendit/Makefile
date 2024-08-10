
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

compose-start:
	docker compose -f docker/docker-compose.yml up