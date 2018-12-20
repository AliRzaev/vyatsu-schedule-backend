# VyatSU schedule API server

[![Build Status](https://travis-ci.org/AliRzaev/vyatsu_schedule_api_server.svg?branch=master)](https://travis-ci.org/AliRzaev/vyatsu_schedule_api_server)

This application provides RESTful API for viewing group schedules.

API documentation can be found here: [vyatsuschedule.github.io/docs](https://vyatsuschedule.github.io/docs)

Designed for [Vyatka State University](https://www.vyatsu.ru)

## Running app

### Required environment variables

`MONGODB_URI` - URI to MongoDB database of format `mongodb://<user>:<password>@<host>:<port>/<database>`. You have to specify the database name.

`REDIS_URI` - URI to Redis database of format `redis://<user>:<password>@<host>:<port>/<database>`. Default database - `0`.

`PORT` - port on which listen requests, default `80`.

`PARSE_API_URL` - URL to [VyatSU schedule PDF parser](https://github.com/AliRzaev/vyatsu_pdf_parser) service.

### Tests

#### Unit tests

`python -m unittest discover -s tests`

#### Integration tests

**Note:** `MONGODB_URI` and `REDIS_URI` must be defined.

**Be attentive!** Some test cases may **wipe out** data in your databases.
Please ensure that you run tests with databases for testing,
not for production.

`python -m unittest discover -s tests -p it*.py`

### Server

`gunicorn -b 0.0.0.0:$PORT server:app`
