FROM python:3.11

# RUN apt-get update && apt-get install docker.io -y
COPY --from=docker:dind /usr/local/bin/docker /usr/local/bin/
RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN mkdir pyjail_ad && touch pyjail_ad/__init__.py README.md && poetry install --no-dev

COPY . .
CMD ["./run.sh"]
