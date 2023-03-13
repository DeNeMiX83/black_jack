include deploy/.env
export $(shell sed 's/=.*//' deploy/.env)

run:
	make run-tg-bot

run-tg-bot:
	poetry run python -m app.presentation.tg_bot.main
	
run-admin-api:
	poetry run python -m app.presentation.admin.main

migrate-create:
	poetry run alembic -c deploy/alembic.ini revision --autogenerate

migrate-up:
	poetry run alembic -c deploy/alembic.ini upgrade head
