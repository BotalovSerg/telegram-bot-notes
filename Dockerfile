FROM python:3.11-slim-bullseye AS builder

COPY poetry.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry && poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt

FROM python:3.11-slim-bullseye AS app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY --from=builder requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY . /app
CMD ["python3", "main.py"]