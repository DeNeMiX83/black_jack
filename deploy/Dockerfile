FROM python:3.11.0
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev --no-root
COPY . ./