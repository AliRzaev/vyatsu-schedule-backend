# VyatSU schedule web server

## Required environment variables

`MONGODB_URI=<uri>` - defines the uri for MongoDB cluster.
Current value: `mongodb://heroku_pwzr1bj8:k43nm5e2vap9o22pubde5bk91a@ds117935.mlab.com:17935/heroku_pwzr1bj8`

`SCHEDULE_CACHE=[enabled|disabled]` - enables or disables caching group schedules in database

## Running app

Required environment variables must be set before running

### Unit tests

`mvn surefire:test`

### Integration tests
**Note:** environment variable MONGODB_URI must be set

`mvn failsafe:integration-test`

### Jar archive

`mvn -DskipTests package`

### Groups info updater

`java -cp target/classes:target/dependency/* rzaevali.updater.GroupsInfoUpdater`

### Date ranges updater

`java -cp target/classes:target/dependency/* rzaevali.updater.DateRangesUpdater [--forced]`

`--forced` - update date ranges regardless of current day or season

### Server

`mvn -DskipTests compile exec:java`