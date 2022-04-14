# Archive Download Service
[![CI](https://github.com/alena-kono/archive-download-service/actions/workflows/ci.yml/badge.svg)](https://github.com/alena-kono/archive-download-service/actions/workflows/ci.yml)

Simple microservice that creates .zip archives on the fly at the request of the user.

## Purpose of this project
This project is an educational one to get familiar with async Python and `aiohttp`.

## Demo
![Demo](demo.gif)

## Requirements
`docker`, `docker compose` should be installed and set up on your machine.

## Installation and running within a Docker container

1. Clone the repo and change the working directory:

    $ cd archive-download-service/

2. Build app:

    $ docker compose build

3. Run app:

    $ docker compose run archive-d-service

4. Archive-download-service is a CLI app. Use `--help` flag to get familiar with the its interface:

    $ docker compose run archive-d-service --help

## Installation and running within poetry environment

1. Clone the repo and change the working directory:

    $ cd archive-download-service/

2. Install main dependencies via poetry:

    $ poetry install --no-dev

**2.1 Optional. Install all the dependencies if you want to develop.**

    $ poetry install

3. Run app:

    $ poetry run archive-d-service

4. Archive-download-service is a CLI app. Use `--help` flag to get familiar with the its interface:

    $ poetry run archive-d-service --help
