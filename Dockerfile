FROM python:3.13.3-slim

COPY --from=ghcr.io/astral-sh/uv:0.6.13 /uv /bin/uv

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONBREAKPOINT=ipdb.set_trace \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    WORKDIR=/app

ENV PATH="$UV_PROJECT_ENVIRONMENT/bin:$PATH" \
    VIRTUAL_ENV=$UV_PROJECT_ENVIRONMENT

WORKDIR $WORKDIR

RUN apt-get update \
    && apt-get install -y build-essential

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ADD . $WORKDIR

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen
