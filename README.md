# Backend-сервер для VyatSU schedule

[![Build Status](https://travis-ci.org/alirzaev/vyatsu-schedule-backend.svg?branch=master)](https://travis-ci.org/alirzaev/vyatsu-schedule-backend)

Данный сервер предоставляет REST API для расписания занятий студентов 
[Вятского государственного университета](https://www.vyatsu.ru).

## Для разработчиков

### Необходимые переменные окружения

`REDIS_URL` - URL базы данных Redis в формате 
`redis://<user>:<password>@<host>:<port>/<database>`.

`PORT` - порт, который сервер будет слушать, по умолчанию `80`.

`PDF2JSON_API_URL` - URL [pdf2json-конвертера](https://github.com/alirzaev/vyatsu-schedule-pdf2json).

### Опционально

`MONGODB_URI` - URI базы данных MongoDB в формате 
`mongodb://<user>:<password>@<host>:<port>/<database>`. 
Поле `<database>` обязательно. Используется для ведения логов.

### Тесты

#### Модульные тесты

`python -m unittest discover -s tests`

#### Интеграционные тесты

**Внимание:** переменные `MONGODB_URI` и `REDIS_URL` должны быть определны.

**Осторожно!** Во время выполнения некоторых тестов данные в БД могут быть 
**безвозвратно** утеряны. 
Перед запуском тестов удостоверьтесь, что используете тестовую базу данных, а не 
основную.

`python -m unittest discover -s tests -p it*.py`

### Запуск

`gunicorn -b 0.0.0.0:$PORT server:app`

### Администрирование

На сайте ВятГУ новое расписание занятий выкладывается каждые две недели. Для того, 
чтобы сервер всегда возвращал актуальное расписание, необходимо не реже, чем 
один раз в две недели обновлять информацию с сайта ВятГУ. Для этого нужно запустить 
следующий скрипт:

`python -m utils.prefetch -f`

Чтобы загрузить информацию только в том случае, если ее нет в БД, то 
запустите скрипт без ключа `-f`.

### Docker

1. Собираем образ

   ```
   docker build -t imagename .
   ```

2. Запускаем
   
   ```
   docker run --name somename -d -p 8080:80 \
     -e MONGODB_URI=<URI> \
     -e REDIS_URL=<URL> \
     -e PDF2JSON_API_URL=<PDF2JSON_API_URL> \
     imagename
   ```
