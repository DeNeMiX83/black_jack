include ./deploy/.env
export $(shell sed 's/=.*//' ./deploy/.env)

DOCKER_COMPOSE := ./deploy/docker-compose.yml
DOCKER_ENV := ./deploy/.env

compose-build:
	docker compose -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) build

compose-up:
	docker compose -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) up

compose-pull:
	docker-compose -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) pull

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
