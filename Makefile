dev:
	uv run uvicorn app:app --reload --host 0.0.0.0 --port 8000

start:
	uv run uvicorn app:app --host 0.0.0.0 --port 8000

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

docker-build:
	docker build -t vaccone-score-backend .

docker-run:
	docker run --rm -p 8000:8000 vaccone-score-backend
