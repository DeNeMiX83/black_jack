include deploy/.env
export $(shell sed 's/=.*//' deploy/.env)

run-admin-api:
	poetry run python -m app.presentation.admin.main