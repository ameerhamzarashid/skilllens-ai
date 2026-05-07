.PHONY: install data ingest quality train pipeline test api streamlit frontend docker-up docker-down clean

install:
	pip install -r requirements.txt

data:
	python -m data_platform.generate_sample_jobs

ingest:
	python -m data_platform.ingest_jobs

quality:
	python -m data_platform.data_quality

train:
	python -m skilllens.ml.train_salary_model
	python -m skilllens.ml.train_category_model

pipeline:
	python -m data_platform.run_pipeline

test:
	python -m pytest

api:
	uvicorn backend.main:app --reload

streamlit:
	streamlit run dashboards/streamlit_app.py

frontend:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-down-volumes:
	docker compose down -v

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"