include deploy/.env
export $(shell sed 's/=.*//' deploy/.env)

DOCKER_ENV := deploy/.env

compose-build:
	docker compose -f ./deploy/prod.docker-compose.yml --env-file DOCKER_ENV build

compose-up:
	docker compose -f ./deploy/prod.docker-compose.yml --env-file DOCKER_ENV up

run-tg-bot:
	poetry run python -m app.presentation.tg_bot.main
	
run-admin-api:
	poetry run python -m app.presentation.admin.main

run-rabbitmq:
	poetry run python -m app.infrastructure.rabbitmq.main

migrate-create:
	poetry run alembic -c deploy/alembic.ini revision --autogenerate

migrate-up:
	poetry run alembic -c deploy/alembic.ini upgrade head
