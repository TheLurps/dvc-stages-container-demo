FROM ghcr.io/astral-sh/uv:python3.12-bookworm

# Copy the project into the image
ADD . /app/

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen

ENTRYPOINT ["uv", "run", "python", "-m"]
