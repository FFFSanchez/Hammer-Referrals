# Hammer Referrals API Service
Реферальная система. Регистрация и авторизация по номеру телефона с подтверждением через 4-х значный код. 
Авторизованному пользователю присваивается 6-ти значный реферальный код. Пользователь может просматривать свой профиль, видеть свой номер телефона, свой реф код, список пользователей которые указали его реф код и может указать реф код человека, который его пригласил. Указать реф код можно только 1 раз. 
Нельзя указывать свой реф код, реф код не существующего пользователя и пользователя который указал ваш реф код в своём профиле.

Функционал реализован как по API так и в браузере через обычные HTML страницы. Авторизация API по токену.

Доступна админка. Также админу доступен уникальный API ендпоинт для просмотра и редактирования всех существующих пользователей.

Сервис задеплоен на серевер Yandex Cloud, CI/CD настроен через GitHub Workflows, используется gunicorn, nginx, docker compose, PostgreSQL.

При успешном завершении actions workflow приходит оповещение в телеграм бот.

Подключен мониторинг UptimeRobot, получен https сертификат.

#### Адрес: https://bigbobs.bounceme.net/
### Стек
+ Django DRF
+ Django Templates
+ PostgreSQL
+ Docker compose
+ Gunicorn
+ Nginx
+ WSL
+ GitHub Workflows CI/CD
+ Yandex Cloud
+ UptimeRobot Monitoring
+ HTTPS Cert
+ Postman

## По проблемам и вопросам запуска писать на https://t.me/lordsanchez
### Как запустить проект:

Клонировать репозиторий:

```
git clone https://github.com/FFFSanchez/Hammer-Referrals.git
```

Добавить свой файл .env в главную папку hammer_refs, в ту же, где Dockerfile (SECRET_KEY можно сгенерить тут https://djecrety.ir/):

```
SECRET_KEY=******

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres

DB_HOST=pgdb
DB_PORT=5432

```

Запуск через docker compose:

```
находясь в одной папке с docker-compose.yml

docker compose -f docker-compose.yml up --build -d
docker compose -f docker-compose.yml exec backend python manage.py migrate
docker compose -f docker-compose.yml exec backend python manage.py collectstatic
docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /app/static_refs_backend/static/

# создать суперюзера если нужен доступ в админку, телефон + пароль
docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

Готово, сервис запущен и доступен на http://localhost:8000/

Админ панель также настроена и доступна по стандарту http://localhost:8000/admin/

# Документация:
Перейти по одной из ссылок:
* http://127.0.0.1:8000/redoc/
* http://127.0.0.1:8000/swagger/

А так же файл schema.yaml в корне проекта

## Примеры запросов к API:
1) Регистрация нового пользователя:
* Отправить POST-запрос http://127.0.0.1:8000/api/v1/auth/signup/. В теле запроса указать: 
```
{
    "phone": "+79999999999"
}
```

На телефон, если он валиден, придет 4-х значный код подтверждения. По умолчанию включен режим фейковой отправки - код придет внутри ответа на запрос, а так же будет отправлен письмом в папку sent_emails в корне проекта. Режим фейковой отправки можно отключить через константу FAKE_CONFIRM в settings.py, тогда внутри ответа кода не будет и при подключении сервиса по отправке смс код будет отправлен на телефон.

2) Получение JWT-токена:
* Отправить POST-запрос http://127.0.0.1:8000/api/v1/auth/token/. В теле запроса указать:
```
{
    "phone": "+79999999999",
    "confirmation_code": "0000"
}
```
* Если код верный, то пользователь будет создан, если он не будет найден в базе. В ответ придёт JWT-токен в форме:

```
{
    "token": "string"
}
```
3) Авторизация:
* Для авторизации в заголовке запросов нужно указывать токен в формате:
```
Bearer *token*
```

4) Получение своего профиля пользователем:
* Отправить GET-запрос http://127.0.0.1:8000/api/v1/my_profile/. 
```
* Ответ придёт в форме:
[
    {
        "phone": "+79872915555",
        "my_refs": [
            {
                "phone": "+79872910111",
            },
            {
                "phone": "+79872912331",
            }
        ],
        "my_inviter": null,
        "my_ref_code": "2ab22f",
        "created_at": "2023-08-20T11:34:28.668199Z"
    }
]
```
5) Указание инвайт 6-ти значного кода. Возможно только если код ранее не указывался, валидный и существует.
* Отправить PATCH-запрос http://127.0.0.1:8000/api/v1/my_profile/. В теле запроса указать:
```
{
    "my_inviter": "69f12d"
}
```

* Ответ придёт в форме(в поле my_inviter будет номер телефона владельца инвайт кода):
```
[
    {
        "phone": "+79872915555",
        "my_refs": [
            {
                "phone": "+79872910111",
            },
            {
                "phone": "+79872912331",
            }
        ],
        "my_inviter": "+79879166903",
        "my_ref_code": "2ab22f",
        "created_at": "2023-08-20T11:34:28.668199Z"
    }
]
```

6) Получение списка всех пользователей (может получить только администратор):

* Отправить GET-запрос http://127.0.0.1:8000/api/v1/all_profiles/
* Ответ придёт в форме списка профилей всех пользователей:

```
{
    "count": 0,
    "next": "http://example.com",
    "previous": "http://example.com",
    "results": [
            {
                "phone": "string",
                "my_refs": "string",
                "my_inviter": "string",
                "my_ref_code": "string",
                "created_at": "2019-08-24T14:15:22Z"
            }
        ]
}
```

## Примеры использования через браузер:
1) Форма авторизации http://127.0.0.1:8000/:
* Указать валидный номер телефона

2) Форма для кода подтверждения http://127.0.0.1:8000/submit/:
* На телефон, если он валиден, придет 4-х значный код подтверждения. По умолчанию включен режим фейковой отправки - код будет отображен в информационном сообщении, а так же будет отправлен письмом в папку sent_emails в корне проекта. Режим фейковой отправки можно отключить через константу FAKE_CONFIRM в settings.py, тогда код на странице отображен не будет и при подключении сервиса по отправке смс код будет отправлен на телефон.

3) Профиль пользователя http://127.0.0.1:8000/my_profile/:
* Отображается номер телефона, список рефералов, свой инвайт код и есть возможнсть указать чужой инвайт код.

4) Логаут пользователя http://127.0.0.1:8000/logout/:
* Выход из аккаунта

5) Админка http://127.0.0.1:8000/admin/:
* Админка. Авторизация по номеру и паролю. Создать админа можно только через manage.py



### Автор: 
Александр Трифонов