DOCKER_COMPOSE := ./deploy/docker-compose.yml
DOCKER_ENV := ./deploy/.env

.PHONY: run-tg-bot
run-tg-bot:
	poetry run python -m app.presentation.tg_bot.main
	
.PHONY: run-admin-api
run-admin-api:
	poetry run python -m app.presentation.admin.main

.PHONY: run-rabbitmq
run-rabbitmq:
	poetry run python -m app.infrastructure.rabbitmq.main

.PHONY: migrate-create
migrate-create:
	poetry run alembic -c deploy/alembic.ini revision --autogenerate

.PHONY: migrate-up
migrate-up:
	poetry run alembic -c deploy/alembic.ini upgrade head

.PHONY: compose-up
compose-up:
	docker-compose -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) up

.PHONY: compose-pull
compose-pull:
	docker-compose -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) pull

.PHONY: compose-down
compose-down:
	docker-compose -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) down
