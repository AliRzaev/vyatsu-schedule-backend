# VyatSU schedule API server

## Required environment variables

`MONGODB_URI=<uri>` - defines the uri for MongoDB cluster.

`PORT` - port on which listen requests, default `8080`

`PARSE_API_URL` - url to VyatSU pdf parser service

## Running app

Required environment variables must be set before running

### Tests

**Be attentive!** Some test cases may **wipe out** data in your database.
Please ensure that you run tests with database for testing,
not for production

`python -m unittest discover -s tests`

### Groups info updater

`python -m updaters.groups_updater`

### Date ranges updater

```
usage: python -m updaters.ranges_updater [-h] [-f] [-d]

optional arguments:
  -h, --help      show this help message and exit
  -f, --force     Update schedule ranges for ALL groups, for ALL seasons
  -d, --drop-old  Delete ALL schedule ranges from DB before updating
```

### Server

`gunicorn -b 0.0.0.0:$PORT server:app`