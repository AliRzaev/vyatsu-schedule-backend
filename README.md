# VyatSU schedule API server

## Required environment variables

`MONGODB_URI=<uri>` - defines the uri for MongoDB cluster.

`SCHEDULE_CACHE=[enabled|disabled]` - enables or disables caching group schedules in database

`PORT` - port on which listen requests, default `8080`

## Running app

Required environment variables must be set before running

### Tests

python -m unittest discover -s tests

### Groups info updater

*TODO*

### Date ranges updater

*TODO*

### Server

`gunicorn -b 0.0.0.0:$PORT server:app`