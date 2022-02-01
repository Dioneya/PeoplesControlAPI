# PeoplesControlAPI

Компоненты API для приложения "Народный Контроль". Данное API было разработано с помощью Python 3.8 и Flask 1.1.2.

## Установка API

1. Клонировать компоненты репозитория в удобное для вас место.
2. Создать вирутальное окружение с помощью virtualenv.
```python
    virtualenv -p python3 envname
```
3. Затем необходимо перейти в созданное виртуальное окружение.
```python
    source ./ИМЯ_ВИРТ_ОКРУЖЕНИЯ/bin/activate # пример для linux
```
4. Установить зависимости компонентов с помощью requirements.txt.
```python
    pip3 install -r requirements.txt
```

5. Импортировать db.sql в базу данных MySQL.
6. Создать юзера для импортированной базы данных с возможность удаления/изменения/создание записей.
7. В файле api.py указать настройки подключения к базе данных в переменной "app.config['SQLALCHEMY_DATABASE_URI']"
```python
    #./api.py

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USER_NAME:PASSWORD@HOST/DATABESE_NAME'
```
7. В переменной DOMAIN_NAME файла api.py укажите текущее домен имя для корректного отобображения данных из некоторых роутов.
```python
    #./api.py

    DOMAIN_NAME = "http://example_domain.com"
```
8. Для работы телеграм бота, необходимо в файле bot.py, расположенного в папке tg изменить переменную bot_token
```python
    #./tg/bot.py

    bot_token = 'UR_BOT_TOKEN'
```

## Запуск API
1. Переходим в виртуально окружение
```python
    source ./ИМЯ_ВИРТ_ОКРУЖЕНИЯ/bin/activate # пример для linux
```
2. Для дебага API, запуск осуществляется с помощью вызова файла api.py.
```python
    python3 api.py
        или
    python api.py
```
===
Для запуска на хостинге рекомендуется запустить с помощью WSGI Gunicorn, предвартительно установив его на сервере.
```python
    pip install gunicorn
```
Затем выполним запуск с помощью команды:
```python
    gunicorn --bind адрес:порт api:app
```

## Список доступных роутов

### Авторизация
#### POST /auth/login
##### Авторизация пользователя в системе
-H: "Content-type":"application/json"

Request Body
```JSON
{
  "username": "0711234444",
  "password": "string"
}
```
Response result 200
```JSON
{
  "accessToken": "ACCESS_TOKEN",
  "refreshToken": "REFRESH_TOKEN",
  "tokenType": "Bearer"
}
```

#### POST /auth/logout  (token required)
##### Выход пользователя из системы


#### POST /auth/refreshtoken  (refresh token required)
##### Обновить токены пользователя

Response result 200
```JSON
{
  "accessToken": "ACCESS_TOKEN",
  "refreshToken": "REFRESH_TOKEN",
  "tokenType": "Bearer"
}
```

#### POST /auth/signup
##### Регистрация нового пользователя

-H: "Content-type":"application/json"

Request Body
```JSON
{
  "name": "Олег",
  "username": "0711234444",
  "password": "string"
}
```
### Сервесные методы



