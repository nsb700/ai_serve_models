install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C webapp/*.py

test:
	python -m pytest -vv --cov=webapp tests/*.py

format:
	black webapp/*.py

createdb:
	alembic upgrade head

installreact:
	cd react/transplants-app && npm install

startuvicorn:
	uvicorn webapp.main:app

startreact:
	cd react/transplants-app/ && npm start

all: install lint test format createdb installreact startuvicorn