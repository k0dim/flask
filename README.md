# Flask

## Общее
Проекте реализована API (`GET`, `POST`, `PATCH`, `DELETE`) для объявлений и системой пользователей.

Для начала работы необходимо создать файл с переменными окружения `.env` в директории [app](app), и заполнить следующим образом:
```
PG_DB=""
PG_USER=""
PG_PASSWORD=""
PG_HOST=""
PG_PORT=""
```
---
## Документация
Запросы приведены в следующей документации:
* Для регистрации пользователя и получения `token`: [User](requests-examples_user.http)
* Для работы с объявлениями: [Ads](requests-examples_ads.http)
---
## Docker
```shell
docker-compose up
```