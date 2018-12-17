# VyatSU schedule API server

This application provides RESTful API for viewing group schedules.

API documentation can be found here: [vyatsuschedule.github.io/docs](https://vyatsuschedule.github.io/docs)

Designed for [Vyatka State University](https://www.vyatsu.ru)

## Running app

### Required environment variables

`MONGODB_URI=<uri>` - URI to MongoDB database of format `mongodb://<user>:<password>@<host>:<port>/<database>`. You have to specify the database name.

`PORT` - port on which listen requests, default `80`.

`PARSE_API_URL` - URL to [VyatSU schedule PDF parser](https://github.com/AliRzaev/vyatsu_pdf_parser) service.

### Tests

#### Unit tests

`python -m unittest discover -s tests`

#### API integration tests

**Note:** `MONGODB_URI` must be defined.

**Be attentive!** Some test cases may **wipe out** data in your database.
Please ensure that you run tests with database for testing,
not for production.

`python -m unittest discover -s tests -p it*.py`

### Scripts for updating information in database

This scripts must be run regulary due to regular changes (every two week) in group schedules on the official [VyatSU](https://vyatsu.ru) site.

#### Groups info updater

`python -m updaters.groups_updater`

#### Date ranges updater

```
usage: python -m updaters.ranges_updater [-h] [-f] [-d]

optional arguments:
  -h, --help      show this help message and exit
  -f, --force     Update schedule ranges for ALL groups, for ALL seasons
  -d, --drop-old  Delete ALL schedule ranges from DB before updating
```

### Server

#### Database initialization

Before running server (only for the first time) you have to load into database information about student groups and date ranges of group schedules.

```
python -m updaters.groups_updater && python -m updaters.ranges_updater
```

#### Running server

`gunicorn -b 0.0.0.0:$PORT server:app`
