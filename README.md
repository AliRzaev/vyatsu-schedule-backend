# VyatSU schedule web server

## Required environment variables

`MONGODB_URI=<uri>` - defines the uri for MongoDB cluster.
Current value: `mongodb://heroku_pwzr1bj8:k43nm5e2vap9o22pubde5bk91a@ds117935.mlab.com:17935/heroku_pwzr1bj8`

`SCHEDULE_CACHE=[enabled|disabled]` - enables or disables caching group schedules in database

## Running app

Required environment variables must be set before running

### Tests

`mvn test`

### Date ranges updater

`java -cp target/classes:target/dependency/* rzaevali.updater.Main`

### Server

`mvn -DskipTests clean package jetty:run`