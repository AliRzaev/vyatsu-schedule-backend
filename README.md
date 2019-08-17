# Backend-сервер для VyatSU schedule

[![Build Status](https://travis-ci.org/alirzaev/vyatsu-schedule-backend.svg?branch=master)](https://travis-ci.org/alirzaev/vyatsu-schedule-backend)

Данный сервер предоставляет REST API для расписания занятий студентов 
[Вятского государственного университета](https://www.vyatsu.ru).

## Для разработчиков

### Необходимые переменные окружения

`FLASK_ENV` - среда запуска: `development`, `testing` и `production`. По 
умолчанию `development`.

#### Production-only
`REDIS_URL` - URL базы данных Redis в формате 
`redis://<user>:<password>@<host>:<port>/<database>`.

`PDF2JSON_API_URL` - URL [pdf2json-конвертера](https://github.com/alirzaev/vyatsu-schedule-pdf2json).

### Опционально

`MONGODB_URI` - URI базы данных MongoDB в формате 
`mongodb://<user>:<password>@<host>:<port>/<database>`. 
Поле `<database>` обязательно. Используется для ведения логов.

### Тесты

#### Модульные тесты

`python -m unittest discover -s tests`

#### Интеграционные тесты

Конфигурация приложения для тестирования: [config.py](config.py)

**Осторожно!** Во время выполнения некоторых тестов данные в БД могут быть 
**безвозвратно** утеряны. 
Перед запуском тестов удостоверьтесь, что используете тестовую базу данных, а не 
основную.

`python -m unittest discover -s tests -p it*.py`

### Запуск 

#### gunicorn

```shell script
export FLASK_ENV=<ENV>
gunicorn -b 0.0.0.0:<PORT> wsgi:app
```

#### development server (werkzeug)

```shell script
export FLASK_ENV=<ENV>
flask run
```

### Администрирование

На сайте ВятГУ новое расписание занятий выкладывается каждые две недели. Для того, 
чтобы сервер всегда возвращал актуальное расписание, необходимо не реже, чем 
один раз в две недели обновлять информацию с сайта ВятГУ. Для этого нужно запустить 
следующий скрипт:

```shell script
export FLASK_ENV=<ENV>
export REDIS_URL=<REDIS_URL>
export PDF2JSON_API_URL=<PDF2JSON_API_URL>
flask prefetch --force
```

Чтобы загрузить информацию только в том случае, если ее нет в БД, то 
запустите скрипт без ключа `--force`.

### Docker

1. Собираем образ

   ```
   docker build -t imagename .
   ```

2. Запускаем
   
   ```
   docker run --name somename -d -p 8080:80 \
     -e FLASK_ENV=<ENV> \
     -e MONGODB_URI=<URI> \
     -e REDIS_URL=<URL> \
     -e PDF2JSON_API_URL=<PDF2JSON_API_URL> \
     imagename
   ```
