# Backend-сервер для VyatSU schedule

[![Build Status](https://travis-ci.org/alirzaev/vyatsu-schedule-backend.svg?branch=master)](https://travis-ci.org/alirzaev/vyatsu-schedule-backend)

Данный сервер предоставляет REST API для расписания занятий студентов 
[Вятского государственного университета](https://www.vyatsu.ru).

Документация по API: [vyatsuschedule.github.io/docs](https://vyatsuschedule.github.io/docs).

## Для разработчиков

### Необходимые переменные окружения

`MONGODB_URI` - URI базы данных MongoDB в формате 
`mongodb://<user>:<password>@<host>:<port>/<database>`. 
Поле `<database>` обязательно.

`PORT` - порт, который сервер будет слушать, по умолчанию `80`.

`PDF2JSON_API_URL` - URL [pdf2json-конвертера](https://gitlab.com/vyatsu-schedule/pdf2json).

### Тесты

#### Модульные тесты

`python -m unittest discover -s tests`

#### Интеграционные тесты

**Внимание:** переменная `MONGODB_URI` должна быть определна.

**Осторожно!** Во время выполнения некоторых тестов данные в БД могут быть 
**безвозвратно** утеряны. 
Перед запуском тестов удостоверьтесь, что используете тестовую базу данных, а не 
основную.

`python -m unittest discover -s tests -p it*.py`

### Запуск

`gunicorn -b 0.0.0.0:$PORT server:app`

### Docker

1. Собираем образ

   ```
   docker build -t imagename .
   ```

2. Запускаем
   
   ```
   docker run --name somename -d -p 8080:80 \
     -e MONGODB_URI=<URI> \
     -e PARSE_API_URL=<PARSE_API_URL> \
     imagename
   ```
