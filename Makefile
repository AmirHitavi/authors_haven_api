build:
	sudo docker-compose -f local.docker-compose.yaml up --build -d

up:
	sudo docker-compose -f local.docker-compose.yaml up -d

down:
	sudo docker-compose -f local.docker-compose.yaml down

logs:
	sudo docker-compose -f local.docker-compose.yaml logs

api_logs:
	sudo docker-compose -f local.docker-compose.yaml logs api

db_logs:
	sudo docker-compose -f local.docker-compose.yaml logs postgres

worker_logs:
	sudo docker-compose -f local.docker-compose.yaml logs worker

makemigrations:
	sudo docker-compose -f local.docker-compose.yaml run --rm api python manage.py makemigrations --no-input
	
migrate:
	sudo docker-compose -f local.docker-compose.yaml run --rm api python manage.py migrate --no-input

collectstatic:
	sudo docker-compose -f local.docker-compose.yaml run --rm api python manage.py collectstatic --no-input --clear

superuser:
	sudo docker-compose -f local.docker-compose.yaml run --rm api python manage.py createsuperuser

down_v:
	sudo docker-compose -f local.docker-compose.yaml down -v

volume:
	sudo docker volume inspect src_local_postgres_data

flake8:
	flake8 .

black:
	black --exclude=migrations .

black-check:
	black --check --exclude=migrations  .

black-diff:
	black --diff --exclude=migrations .

isort:
	isort . --skip venv --skip migrations

isort-check:
	isort . --check-only --skip venv --skip migrations

isort-diff:
	isort . --diff --skip venv --skip migrations

shell:
	sudo docker-compose -f local.docker-compose.yaml exec api /bin/bash

backup:
	sudo docker-compose -f local.docker-compose.yaml exec postgres backup

backups:
	sudo docker-compose -f local.docker-compose.yaml exec postgres backups

status:
	sudo docker ps

es-create:
	sudo docker-compose -f local.docker-compose.yaml exec api python manage.py search_index --create

es-populate:
	sudo docker-compose -f local.docker-compose.yaml exec api python manage.py search_index --populate
