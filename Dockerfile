FROM python:3.9

RUN apt-get update
RUN apt-get install zip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/archive_download_service

COPY /archive_download_service /app/archive_download_service
COPY pyproject.toml poetry.lock /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8080

CMD ["poetry", "run", "python", "-m", "archive_download_service.server"]
