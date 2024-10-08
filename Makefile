build:
	docker-compose -f local.docker-compose.yaml up --build -d

up:
	docker-compose -f local.docker-compose.yaml up -d

down:
	docker-compose -f local.docker-compose.yaml down

logs:
	docker-compose -f local.docker-compose.yaml logs

api_logs:
	docker-compose -f local.docker-compose.yaml logs api

db_logs:
	docker-compose -f local.docker-compose.yaml logs postgres

worker_logs:
	docker-compose -f local.docker-compose.yaml logs worker

makemigrations:
	docker-compose -f local.docker-compose.yaml run --rm api python manage.py makemigrations --no-input
	
migrate:
	docker-compose -f local.docker-compose.yaml run --rm api python manage.py migrate --no-input

collectstatic:
	docker-compose -f local.docker-compose.yaml run --rm api python manage.py collectstatic --no-input --clear

superuser:
	docker-compose -f local.docker-compose.yaml run --rm api python manage.py createsuperuser

down_v:
	docker-compose -f local.docker-compose.yaml down -v

volume:
	docker volume inspect src_local_postgres_data

flake8:
	flake8 .

black:
	black --exclude=migrations .

black-check:
	black --check --exclude=migrations .

black-diff:
	black --diff --exclude=migrations .

isort:
	isort . --skip venv --skip migrations

isort-check:
	isort . --check-only --skip venv --skip migrations

isort-diff:
	isort . --diff --skip venv --skip migrations


shell:
	docker-compose -f local.docker-compose.yaml exec api /bin/bash

backup:
	docker-compose -f local.docker-compose.yaml exec postgres backup

backups:
	docker-compose -f local.docker-compose.yaml exec postgres backups

status:
	docker ps

es-create:
	docker-compose -f local.docker-compose.yaml exec api python manage.py search_index --create

es-populate:
	docker-compose -f local.docker-compose.yaml exec api python manage.py search_index --populate

es-delete:
	docker-compose -f local.docker-compose.yaml exec api python manage.py search_index --delete