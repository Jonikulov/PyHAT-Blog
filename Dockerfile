# --------------- Stage 1: Build ---------------
FROM python:3.13-slim-trixie AS builder

# System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext && \
    rm -rf /var/lib/apt/lists/*
# Install uv binary
COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
    # Set uv to use the container's native Python and stop downloading
    UV_PYTHON_PREFERENCE=only-system \
    # Forbid uv from ever downloading Python at runtime
    UV_PYTHON_DOWNLOADS=never \
    # Enable bytecode compilation
    UV_COMPILE_BYTECODE=1 \
    # Copy from the cache instead of linking
    UV_LINK_MODE=copy

WORKDIR /app
# Install dependencies without the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    # uv sync --locked --no-default-groups --no-install-project
    uv sync --locked --no-install-project

# Copy the rest of the project & sync & install them
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    # uv sync --locked --no-default-groups
    uv sync --locked


# --------------- Stage 2: Production ---------------
FROM python:3.13-slim-trixie AS final

# System deps & delete everything not needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext && \
    # apt-get purge --auto-remove -y wget curl telnet netcat-openbsd && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /bin/su /usr/bin/passwd   # remove escalation tools

# Setup a non-root user
RUN groupadd --system --gid 999 django && \
    useradd --system --gid 999 --uid 999 --create-home django

COPY --from=builder --chown=django:django /app /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH="/app/.venv/bin:$PATH"

# Create directories & ensure scripts are executable
RUN mkdir -p /app/staticfiles && \
    chown -R django:django /app/staticfiles && \
    chmod -R 755 /app/staticfiles && \
    chmod +x /app/setup-django.sh
# RUN chmod +x /app/setup-django.sh

WORKDIR /app
USER django

EXPOSE 8000
ENTRYPOINT [ "/app/setup-django.sh" ]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
