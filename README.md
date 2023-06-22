# Testing Workshop

Template project for a workshop that covers how to write tests and code together, how to run tests and
automate test running on collaborative projects.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Note

- This is an example app that should _not_ be run in production.

## Quick Start

Here are the steps to run the Django app locally in development mode.

### Prerequisites

This application runs in containers on Docker with Docker Compose. You should have installed Docker and Docker Compose.

### Build the Code

Clone this repository:

`$ git clone https://github.com/mchesterkadwell/testing_workshop.git`

Build the Docker stack with the local configuration. This make take a few minutes:

`$ docker compose -f local.yml build`

### Run the Application

Run the Docker stack with the local configuration:

`$ docker compose -f local.yml up`

You can view the web application locally at: http://localhost:8000/

### Run the Tests

To run the tests:

`$ docker compose -f local.yml run --rm django pytest`

To generate an HTML coverage report:

`$ docker compose -f local.yml run --rm django coverage html`

Now you can view the report by opening it in a browser: `htmlcov/index.html`

### Optional

Run the database migrations. They should run on startup, but just in case you can do it manually:

`$ docker compose -f local.yml run --rm django python manage.py migrate`

Create a superuser. It is not important what you choose here as we do not use authentication in the application:

`$ docker compose -f local.yml run --rm django python manage.py createsuperuser`
