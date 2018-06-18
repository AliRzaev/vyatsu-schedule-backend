# VyatSU schedule API server

## Required environment variables

`MONGODB_URI=<uri>` - defines the uri for MongoDB cluster.

`SCHEDULE_CACHE=[enabled|disabled]` - enables or disables caching group schedules in database

`PORT` - port on which listen requests, default `8080`

`PARSE_API_URL` - url to VyatSU pdf parser service

## Running app

Required environment variables must be set before running

### Tests

Note: do not run tests with production db. It may delete all information

`python -m unittest discover -s tests`

### Groups info updater

`python -m updaters.groups_updater`

### Date ranges updater

*TODO*

### Server

`gunicorn -b 0.0.0.0:$PORT server:app`