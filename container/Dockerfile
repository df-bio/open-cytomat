# syntax=docker/dockerfile:1.7
FROM ghcr.io/astral-sh/uv:python3.10-trixie

ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=never
ENV APP_DIR=/opt/open-cytomat
ENV PATH=${APP_DIR}/.venv/bin:${PATH}

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_DIR}

# Copy metadata first so dependency layers survive normal source edits.
COPY pyproject.toml poetry.lock README.md ${APP_DIR}/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv ${APP_DIR}/.venv

COPY src/ ${APP_DIR}/src/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --python ${APP_DIR}/.venv/bin/python ".[sila]"

ENTRYPOINT ["open-cytomat"]
CMD ["--help"]
