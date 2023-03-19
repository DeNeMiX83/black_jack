DOCKER_COMPOSE := deploy/docker-compose.yml
DOCKER_ENV := deploy/.env
DOCKER_COMPOSE_RUNNER := docker compose

ifneq ($(ENV),)
	DOCKER_COMPOSE := deploy/dev.docker-compose.yml
	DOCKER_ENV := deploy/.env.dev
	DOCKER_COMPOSE_RUNNER := docker compose
	include deploy/.env.dev
	export $(shell sed 's/=.*//' deploy/.env.dev)
endif


.PHONY: run-tg-bot
run-tg-bot:
	poetry run python -m app.presentation.tg_bot.main
	
.PHONY: run-api
run-api:
	poetry run python -m app.presentation.api.main

.PHONY: run-tg-poller
run-tg-poller:
	poetry run python -m app.infrastructure.rabbitmq.main

.PHONY: migrate-create
migrate-create:
	poetry run alembic -c deploy/alembic.ini revision --autogenerate

.PHONY: migrate-up
migrate-up:
	poetry run alembic -c deploy/alembic.ini upgrade head

.PHONY: compose-up
compose-up:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) up

.PHONY: compose-build
compose-build:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) build

.PHONY: compose-pull
compose-pull:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) pull

.PHONY: compose-down
compose-down:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) down

.PHONY: compose-logs
compose-logs:
	$(DOCKER_COMPOSE_RUNNER) -f $(DOCKER_COMPOSE) --env-file $(DOCKER_ENV) logs -f