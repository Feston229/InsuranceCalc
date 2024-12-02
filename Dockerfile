FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk add --no-cache \
  gcc \
  musl-dev \
  python3-dev \
  libffi-dev \
  openssl-dev \
  build-base \
  linux-headers \
  zlib-dev

RUN pip install uv==0.5.4

# Copying requirements of a project
COPY pyproject.toml /app/src/
COPY uv.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN uv sync --frozen --no-dev
COPY . /app/src/
RUN uv build .

# Run migrations, deploy seed and start the application
CMD uv run --frozen --no-dev alembic upgrade head && \
  uv run --frozen --no-dev python -m insurance_calc deploy && \
  uv run --frozen --no-dev python -m insurance_calc run
