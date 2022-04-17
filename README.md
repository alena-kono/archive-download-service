# Archive Download Service
[![CI](https://github.com/alena-kono/archive-download-service/actions/workflows/ci.yml/badge.svg)](https://github.com/alena-kono/archive-download-service/actions/workflows/ci.yml)

Simple microservice that creates .zip archives on the fly at the request of the user.

## Purpose of this project
This project is an educational one to get familiar with async `python` and `aiohttp`.

## Usage

    $ GET /archive/{archive_name}

For example, to download zip archive using `curl`:

    $ curl http://localhost:8080/archive/{archive_name} --output {archive_name}.zip

## CLI
Archive-download-service has the CLI that allows to:
- enable logging;
- specify response delay time in seconds;
- specify the path to the files directory.


```
$ docker compose run archive-d-service --help

usage: archive-d-service [-h] [-p [path]] [-l] [-d [secs_float]]

Simple microservice that creates .zip archives on the fly at the request of the user.

optional arguments:
  -h, --help            show this help message and exit
  -p [path], --path [path]
                        Path to files directory.
  -l, --logging         Enable logging.
  -d [secs_float], --delay [secs_float]
                        Response delay in seconds.
```

## Installation and running within a Docker container
### Requirements
`docker`, `docker compose` should be installed and set up on your machine.

1. Clone the repo and change the working directory:

        $ cd archive-download-service/

2. Build app:

        $ docker compose build

3. Run app:

        $ docker compose run archive-d-service

4. Use `--help` flag to get familiar with the CLI interface:

        $ docker compose run archive-d-service --help

## Installation and running within poetry environment
### Requirements
`poetry` should be installed and set up on your machine.

1. Clone the repo and change the working directory:

        $ cd archive-download-service/

2. Install main dependencies via poetry:

        $ poetry install --no-dev

    *2.1 Optional. Install all the dependencies if you want to develop:*

        $ poetry install

3. Run app:

        $ poetry run archive-d-service

4. Use `--help` flag to get familiar with the CLI interface:

        $ poetry run archive-d-service --help
