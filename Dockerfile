FROM python:3.12.3-slim

ARG DEBIAN_FRONTEND=noninteractive

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONBREAKPOINT=ipdb.set_trace \
    POETRY_VERSION=1.7.1 \
    POETRY_VIRTUALENVS_CREATE="false" \
    POETRY_ACCEPT="true" \
    POETRY_HOME="/opt/poetry" \
    WORKDIR=/code

ENV PYTHONPATH=$WORKDIR

WORKDIR $WORKDIR

RUN apt-get update \
    && apt-get install -y curl build-essential

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s ${POETRY_HOME}/bin/poetry /usr/bin/poetry

COPY poetry.lock pyproject.toml $WORKDIR/
RUN poetry install --no-root

COPY . $WORKDIR/
