# PeoplesControlAPI

Компоненты API для приложения "Народный Контроль". Данное API было разработано с помощью Python 3.8 и Flask 1.1.2.

## **Установка API**

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

## **Запуск API**
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

## **Список доступных роутов**

### **Авторизация**
#### **POST /auth/login**
##### **Авторизация пользователя в системе**
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

#### **POST /auth/logout  (token required)**
##### **Выход пользователя из системы**


#### **POST /auth/refreshtoken  (refresh token required)**
##### **Обновить токены пользователя**

Response result 200
```JSON
{
  "accessToken": "ACCESS_TOKEN",
  "refreshToken": "REFRESH_TOKEN",
  "tokenType": "Bearer"
}
```

#### **POST /auth/signup**
##### **Регистрация нового пользователя**

-H: "Content-type":"application/json"

Request Body
```JSON
{
  "name": "Олег",
  "username": "0711234444",
  "password": "string"
}
```
### **Сервесные методы**
#### **POST /services/address**
##### **Получение адреса по координатам**

-H: "Content-type":"application/json"

Request Body
```JSON
{
  "latitude": "23.4445555",
  "longitude": "35.2233444"
}
```
Response result 200
```JSON
{
  "address": "г. Донецк, пр. Киевский, 28"
}
```

#### **POST /services/coords**
##### **Получение координат по адресу**

-H: "Content-type":"application/json"

Request Body
```JSON
{
  "address": "г. Донецк, пр. Киевский, 28"
}
```
Response result 200
```JSON
{
  "latitude": "23.4445555",
  "longitude": "35.2233444"
}
```

### **Профили пользователей**
#### **GET /profiles (token required)**
##### **Список профилей**
(СПИСОК МОЖЕТ ПОЛУЧИТЬ ТОЛЬКО АДМИНЫ)
url params:

page - (integer) номер страницы результата.
size - (integer) количество выводимых записей результата на страницу.

Response result 200
```JSON
{
  "links": {
    "first": "http://localhost:8000/api/{method_name}?page=1",
    "last": "http://localhost:8000/api/{method_name}?page=1",
    "prev": "http://localhost:8000/api/{method_name}?page=1",
    "next": "http://localhost:8000/api/{method_name}?page=1"
  },
  "current_page": 1,
  "from": 1,
  "last_page": 1,
  "path": "http://localhost:8000/api/{method_name}",
  "per_page": 30,
  "to": 1,
  "total": 10,
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "full_name": "Алексей Алексеевич Алексеев",
      "location": "Донецк, Куйбышевский район",
      "phone": "07143200000",
      "rating": 1023,
      "email": "test@test.com",
      "requests": [
        {
          "id": 1,
          "parent_request_id": 1,
          "description": "Бродячие собаки",
          "source": "ANDROID",
          "problem_categories": [
            {
              "id": 1,
              "title": "Яма на дороге",
              "mnemonic_name": "yama_na_doroge",
              "hash_tag": "#дорожное_движение",
              "icon": "https://test.com/123.jpg",
              "rating": 10,
              "is_active": true,
              "is_visible": true,
              "deleted_at": "2022-01-01 12:00:00",
              "created_at": "2022-01-01 12:00:00",
              "updated_at": "2022-01-01 12:00:00"
            }
          ],
          "location": "г. Донецк, пр. Труда, 23",
          "latitude": 23.2334444,
          "longitude": 45.7889111,
          "base_rating": 613,
          "rating": 613,
          "watch_count": 613,
          "status": "IN PROCESSING",
          "attachments": [],
          "stored_profile_data": {
            "full_name": "Алексей Алексеевич Алексеев",
            "location": "Донецк, Куйбышевский район",
            "phone": "07143200000",
            "rating": 1023,
            "email": "test@test.com"
          },
          "request_consideration_at": "2022-02-03 13:00:00",
          "begin_request_execution_at": "2022-02-03 13:00:00",
          "complete_request_execution_at": "2022-02-03 13:00:00",
          "request_status_checked_at": "2022-02-03 13:00:00",
          "is_moderated": true,
          "moderator_id": 1,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "stored_requests": [
        {
          "id": 1,
          "user_id": 1,
          "description": "Описание заявки",
          "problem_categories": [
            {
              "id": 1,
              "title": "Яма на дороге",
              "mnemonic_name": "yama_na_doroge",
              "hash_tag": "#дорожное_движение",
              "icon": "https://test.com/123.jpg",
              "rating": 10,
              "is_active": true,
              "is_visible": true,
              "deleted_at": "2022-01-01 12:00:00",
              "created_at": "2022-01-01 12:00:00",
              "updated_at": "2022-01-01 12:00:00"
            }
          ],
          "latitude": 23.2334444,
          "longitude": 45.7889111,
          "attachments": [],
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "is_notification_email": true,
      "is_notification_sms": true,
      "is_anonymous_requests": false,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ]
}
```


#### **GET /profiles/(id) (token required)**
##### **Получить профиль по ID профиля**
ДОСТУП МОЖЕТ ЛИШЬ ПОЛУЧИТЬ ВЛАДЕЛЕЦ ПРОФИЛЯ ИЛИ АДМИНЫ

Response result 200
```JSON
{
  "id": 1,
  "user_id": 1,
  "full_name": "Алексей Алексеевич Алексеев",
  "location": "Донецк, Куйбышевский район",
  "phone": "07143200000",
  "rating": 1023,
  "email": "test@test.com",
  "requests": [
    {
      "id": 1,
      "parent_request_id": 1,
      "description": "Бродячие собаки",
      "source": "ANDROID",
      "problem_categories": [
        {
          "id": 1,
          "title": "Яма на дороге",
          "mnemonic_name": "yama_na_doroge",
          "hash_tag": "#дорожное_движение",
          "icon": "https://test.com/123.jpg",
          "rating": 10,
          "is_active": true,
          "is_visible": true,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "location": "г. Донецк, пр. Труда, 23",
      "latitude": 23.2334444,
      "longitude": 45.7889111,
      "base_rating": 613,
      "rating": 613,
      "watch_count": 613,
      "status": "IN PROCESSING",
      "attachments": [],
      "stored_profile_data": {
        "full_name": "Алексей Алексеевич Алексеев",
        "location": "Донецк, Куйбышевский район",
        "phone": "07143200000",
        "rating": 1023,
        "email": "test@test.com"
      },
      "request_consideration_at": "2022-02-03 13:00:00",
      "begin_request_execution_at": "2022-02-03 13:00:00",
      "complete_request_execution_at": "2022-02-03 13:00:00",
      "request_status_checked_at": "2022-02-03 13:00:00",
      "is_moderated": true,
      "moderator_id": 1,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "stored_requests": [
    {
      "id": 1,
      "user_id": 1,
      "description": "Описание заявки",
      "problem_categories": [
        {
          "id": 1,
          "title": "Яма на дороге",
          "mnemonic_name": "yama_na_doroge",
          "hash_tag": "#дорожное_движение",
          "icon": "https://test.com/123.jpg",
          "rating": 10,
          "is_active": true,
          "is_visible": true,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "latitude": 23.2334444,
      "longitude": 45.7889111,
      "attachments": [],
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "is_notification_email": true,
  "is_notification_sms": true,
  "is_anonymous_requests": false,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```

#### **GET /profile (token required)**
##### **Получить профиль пользователя по id токена**
Response result 200
```JSON
{
  "id": 1,
  "user_id": 1,
  "full_name": "Алексей Алексеевич Алексеев",
  "location": "Донецк, Куйбышевский район",
  "phone": "07143200000",
  "rating": 1023,
  "email": "test@test.com",
  "requests": [
    {
      "id": 1,
      "parent_request_id": 1,
      "description": "Бродячие собаки",
      "source": "ANDROID",
      "problem_categories": [
        {
          "id": 1,
          "title": "Яма на дороге",
          "mnemonic_name": "yama_na_doroge",
          "hash_tag": "#дорожное_движение",
          "icon": "https://test.com/123.jpg",
          "rating": 10,
          "is_active": true,
          "is_visible": true,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "location": "г. Донецк, пр. Труда, 23",
      "latitude": 23.2334444,
      "longitude": 45.7889111,
      "base_rating": 613,
      "rating": 613,
      "watch_count": 613,
      "status": "IN PROCESSING",
      "attachments": [],
      "stored_profile_data": {
        "full_name": "Алексей Алексеевич Алексеев",
        "location": "Донецк, Куйбышевский район",
        "phone": "07143200000",
        "rating": 1023,
        "email": "test@test.com"
      },
      "request_consideration_at": "2022-02-03 13:00:00",
      "begin_request_execution_at": "2022-02-03 13:00:00",
      "complete_request_execution_at": "2022-02-03 13:00:00",
      "request_status_checked_at": "2022-02-03 13:00:00",
      "is_moderated": true,
      "moderator_id": 1,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "stored_requests": [
    {
      "id": 1,
      "user_id": 1,
      "description": "Описание заявки",
      "problem_categories": [
        {
          "id": 1,
          "title": "Яма на дороге",
          "mnemonic_name": "yama_na_doroge",
          "hash_tag": "#дорожное_движение",
          "icon": "https://test.com/123.jpg",
          "rating": 10,
          "is_active": true,
          "is_visible": true,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "latitude": 23.2334444,
      "longitude": 45.7889111,
      "attachments": [],
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "is_notification_email": true,
  "is_notification_sms": true,
  "is_anonymous_requests": false,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```
#### **PUT /profiles/(id) (token required)**
##### **Изменить профиль по ID профиля**
ДОСТУП МОЖЕТ ЛИШЬ ПОЛУЧИТЬ ВЛАДЕЛЕЦ ПРОФИЛЯ ИЛИ АДМИНЫ

-H: "Content-type":"application/json"

Request Body
```JSON
{
  "user_id": 1,
  "full_name": "Алексей Алексеевич Алексеев",
  "location": "Донецк, Куйбышевский район",
  "phone": "07143200000",
  "email": "test@test.com",
  "is_notification_email": true,
  "is_notification_sms": true,
  "is_anonymous_requests": false
}
```
Response result 200
```JSON
{
  "id": 1,
  "user_id": 1,
  "full_name": "Алексей Алексеевич Алексеев",
  "location": "Донецк, Куйбышевский район",
  "phone": "07143200000",
  "rating": 1023,
  "email": "test@test.com",
  "requests": [
    {
      "id": 1,
      "parent_request_id": 1,
      "description": "Бродячие собаки",
      "source": "ANDROID",
      "problem_categories": [
        {
          "id": 1,
          "title": "Яма на дороге",
          "mnemonic_name": "yama_na_doroge",
          "hash_tag": "#дорожное_движение",
          "icon": "https://test.com/123.jpg",
          "rating": 10,
          "is_active": true,
          "is_visible": true,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "location": "г. Донецк, пр. Труда, 23",
      "latitude": 23.2334444,
      "longitude": 45.7889111,
      "base_rating": 613,
      "rating": 613,
      "watch_count": 613,
      "status": "IN PROCESSING",
      "attachments": [],
      "stored_profile_data": {
        "full_name": "Алексей Алексеевич Алексеев",
        "location": "Донецк, Куйбышевский район",
        "phone": "07143200000",
        "rating": 1023,
        "email": "test@test.com"
      },
      "request_consideration_at": "2022-02-03 13:00:00",
      "begin_request_execution_at": "2022-02-03 13:00:00",
      "complete_request_execution_at": "2022-02-03 13:00:00",
      "request_status_checked_at": "2022-02-03 13:00:00",
      "is_moderated": true,
      "moderator_id": 1,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "stored_requests": [
    {
      "id": 1,
      "user_id": 1,
      "description": "Описание заявки",
      "problem_categories": [
        {
          "id": 1,
          "title": "Яма на дороге",
          "mnemonic_name": "yama_na_doroge",
          "hash_tag": "#дорожное_движение",
          "icon": "https://test.com/123.jpg",
          "rating": 10,
          "is_active": true,
          "is_visible": true,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "latitude": 23.2334444,
      "longitude": 45.7889111,
      "attachments": [],
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "is_notification_email": true,
  "is_notification_sms": true,
  "is_anonymous_requests": false,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```

#### **DELETE /profiles/(id) (token required)**
##### **Удалить профиль пользователя по id токена**
ДОСТУП МОЖЕТ ПОЛЧИТЬ ТОЛЬКО ВЛАДЕЮЩИЙ ПРОФИЛЕМ ПОЛЬЗОВАТЕЛЬ ИЛИ АДМИНЫ

Response result 200
```JSON
{
  "id": 1,
  "user_id": 1,
  "full_name": "Алексей Алексеевич Алексеев",
  "location": "Донецк, Куйбышевский район",
  "phone": "07143200000",
  "rating": 1023,
  "email": "test@test.com",
  "requests": [
    {
      "id": 1,
      "parent_request_id": 1,
      "description": "Бродячие собаки",
      "source": "ANDROID",
      "problem_categories": [
        {
          "id": 1,
          "title": "Яма на дороге",
          "mnemonic_name": "yama_na_doroge",
          "hash_tag": "#дорожное_движение",
          "icon": "https://test.com/123.jpg",
          "rating": 10,
          "is_active": true,
          "is_visible": true,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "location": "г. Донецк, пр. Труда, 23",
      "latitude": 23.2334444,
      "longitude": 45.7889111,
      "base_rating": 613,
      "rating": 613,
      "watch_count": 613,
      "status": "IN PROCESSING",
      "attachments": [],
      "stored_profile_data": {
        "full_name": "Алексей Алексеевич Алексеев",
        "location": "Донецк, Куйбышевский район",
        "phone": "07143200000",
        "rating": 1023,
        "email": "test@test.com"
      },
      "request_consideration_at": "2022-02-03 13:00:00",
      "begin_request_execution_at": "2022-02-03 13:00:00",
      "complete_request_execution_at": "2022-02-03 13:00:00",
      "request_status_checked_at": "2022-02-03 13:00:00",
      "is_moderated": true,
      "moderator_id": 1,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "stored_requests": [
    {
      "id": 1,
      "user_id": 1,
      "description": "Описание заявки",
      "problem_categories": [
        {
          "id": 1,
          "title": "Яма на дороге",
          "mnemonic_name": "yama_na_doroge",
          "hash_tag": "#дорожное_движение",
          "icon": "https://test.com/123.jpg",
          "rating": 10,
          "is_active": true,
          "is_visible": true,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "latitude": 23.2334444,
      "longitude": 45.7889111,
      "attachments": [],
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "is_notification_email": true,
  "is_notification_sms": true,
  "is_anonymous_requests": false,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```

### **Роли**
#### **GET /roles**
##### **Списки ролей пользователей**

(СПИСОК МОЖЕТ ПОЛУЧИТЬ ТОЛЬКО АДМИНЫ)
url params:

page - (integer) номер страницы результата.
size - (integer) количество выводимых записей результата на страницу.

Response result 200
```JSON
{
  "links": {
    "first": "http://localhost:8000/api/{method_name}?page=1",
    "last": "http://localhost:8000/api/{method_name}?page=1",
    "prev": "http://localhost:8000/api/{method_name}?page=1",
    "next": "http://localhost:8000/api/{method_name}?page=1"
  },
  "current_page": 1,
  "from": 1,
  "last_page": 1,
  "path": "http://localhost:8000/api/{method_name}",
  "per_page": 30,
  "to": 1,
  "total": 10,
  "data": [
    {
      "id": 1,
      "title": "GUEST",
      "slug": "guest",
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ]
```

#### **GET /roles/(id)**
##### **Получить роль пользователей по ID**

(МОЖЕТ ПОЛУЧИТЬ ТОЛЬКО АДМИН)

Response result 200
```JSON
{
    "id": 1,
    "title": "GUEST",
    "slug": "guest",
    "deleted_at": "2022-01-01 12:00:00",
    "created_at": "2022-01-01 12:00:00",
    "updated_at": "2022-01-01 12:00:00"
}
```
#### **PUT /roles/(id)**
##### **Редактировать роль пользователя по ID**

(МОЖЕТ ТОЛЬКО АДМИН)

Request body
```JSON
{
  "title": "GUEST",
  "slug": "guest"
}
```

Response result 200
```JSON
{
    "id": 1,
    "title": "GUEST",
    "slug": "guest",
    "deleted_at": "2022-01-01 12:00:00",
    "created_at": "2022-01-01 12:00:00",
    "updated_at": "2022-01-01 12:00:00"
}
```

#### **DELETE /roles/(id)**
##### **Удалить роль пользователя по ID**

(МОЖЕТ ТОЛЬКО АДМИН)

Response result 200
```JSON
{
    "id": 1,
    "title": "GUEST",
    "slug": "guest",
    "deleted_at": "2022-01-01 12:00:00",
    "created_at": "2022-01-01 12:00:00",
    "updated_at": "2022-01-01 12:00:00"
}
```

#### **POST /roles**
##### **Создать роль пользователя по ID**

(МОЖЕТ ТОЛЬКО АДМИН)

Request body
```JSON
{
  "title": "GUEST",
  "slug": "guest"
}
```

Response result 200
```JSON
{
    "id": 1,
    "title": "GUEST",
    "slug": "guest",
    "deleted_at": "2022-01-01 12:00:00",
    "created_at": "2022-01-01 12:00:00",
    "updated_at": "2022-01-01 12:00:00"
}
```

### **Исполнительные органы**
#### **GET /contractors**
##### **Список исполнительных органов**

url params:

page - (integer) номер страницы результата.
size - (integer) количество выводимых записей результата на страницу.

Response result 200
```JSON
{
  "links": {
    "first": "http://localhost:8000/api/{method_name}?page=1",
    "last": "http://localhost:8000/api/{method_name}?page=1",
    "prev": "http://localhost:8000/api/{method_name}?page=1",
    "next": "http://localhost:8000/api/{method_name}?page=1"
  },
  "current_page": 1,
  "from": 1,
  "last_page": 1,
  "path": "http://localhost:8000/api/{method_name}",
  "per_page": 30,
  "to": 1,
  "total": 10,
  "data": [
    {
      "id": 1,
      "mnemonic_name": "mvd",
      "title": "Министерство внутренних дел",
      "description": "Министерство внутренних дел - контролирующий орган",
      "responsible_person": "Петров В.В., старший лейтинант",
      "image": "avatar.jpg",
      "hash_tag": "#мвд",
      "contact_phone": "0713333333",
      "contact_email": "mvd@mvd.com",
      "pre_controller_email": "mvd@mvd.com",
      "telegram_chat_id": "-10000000001",
      "public_website": "https://mvd.com",
      "more_info": "На службе добра",
      "type": "EXECUTIVE",
      "schedule": [
        {
          "title": "Понедельник",
          "day_index": "1",
          "start_at": "09:00",
          "end_at": "18:00",
          "is_day_of": "Флаг выходного дня",
          "description": "Только прием документов"
        }
      ],
      "problem_categories": [
        {
          "id": 1,
          "title": "Яма на дороге",
          "mnemonic_name": "yama_na_doroge",
          "hash_tag": "#дорожное_движение",
          "icon": "https://test.com/123.jpg",
          "rating": 10,
          "is_active": true,
          "is_visible": true,
          "deleted_at": "2022-01-01 12:00:00",
          "created_at": "2022-01-01 12:00:00",
          "updated_at": "2022-01-01 12:00:00"
        }
      ],
      "is_active": true,
      "generate_daily_report": true,
      "need_inform_by_email": true,
      "need_inform_by_sms": true,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ]
}
```

#### **GET /contractors/(id)**
##### **Получить данные об исполнительном органе по ID**

Response result 200
```JSON
{
  "id": 1,
  "mnemonic_name": "mvd",
  "title": "Министерство внутренних дел",
  "description": "Министерство внутренних дел - контролирующий орган",
  "responsible_person": "Петров В.В., старший лейтинант",
  "image": "avatar.jpg",
  "hash_tag": "#мвд",
  "contact_phone": "0713333333",
  "contact_email": "mvd@mvd.com",
  "pre_controller_email": "mvd@mvd.com",
  "telegram_chat_id": "-10000000001",
  "public_website": "https://mvd.com",
  "more_info": "На службе добра",
  "type": "EXECUTIVE",
  "schedule": [
    {
      "title": "Понедельник",
      "day_index": "1",
      "start_at": "09:00",
      "end_at": "18:00",
      "is_day_of": "Флаг выходного дня",
      "description": "Только прием документов"
    }
  ],
  "problem_categories": [
    {
      "id": 1,
      "title": "Яма на дороге",
      "mnemonic_name": "yama_na_doroge",
      "hash_tag": "#дорожное_движение",
      "icon": "https://test.com/123.jpg",
      "rating": 10,
      "is_active": true,
      "is_visible": true,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "is_active": true,
  "generate_daily_report": true,
  "need_inform_by_email": true,
  "need_inform_by_sms": true,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```
#### **PUT /contractors/(id)**
##### **Редактировать данные об исполнительном органе по ID**

(МОЖЕТ ТОЛЬКО АДМИН)

Request body
```JSON
{
  "mnemonic_name": "mvd",
  "title": "Министерство внутренних дел",
  "description": "Министерство внутренних дел - контролирующий орган",
  "responsible_person": "Петров В.В., старший лейтинант",
  "image": "avatar.jpg",
  "hash_tag": "#мвд",
  "contact_phone": "0713333333",
  "contact_email": "mvd@mvd.com",
  "pre_controller_email": "mvd@mvd.com",
  "telegram_chat_id": "-10000000001",
  "public_website": "https://mvd.com",
  "more_info": "На службе добра",
  "type": "EXECUTIVE",
  "schedule": [],
  "problem_categories": [
    1,
    2,
    3,
    4
  ],
  "is_active": true,
  "generate_daily_report": true,
  "need_inform_by_email": true,
  "need_inform_by_sms": true
}
```

Response result 200
```JSON
{
  "id": 1,
  "mnemonic_name": "mvd",
  "title": "Министерство внутренних дел",
  "description": "Министерство внутренних дел - контролирующий орган",
  "responsible_person": "Петров В.В., старший лейтинант",
  "image": "avatar.jpg",
  "hash_tag": "#мвд",
  "contact_phone": "0713333333",
  "contact_email": "mvd@mvd.com",
  "pre_controller_email": "mvd@mvd.com",
  "telegram_chat_id": "-10000000001",
  "public_website": "https://mvd.com",
  "more_info": "На службе добра",
  "type": "EXECUTIVE",
  "schedule": [
    {
      "title": "Понедельник",
      "day_index": "1",
      "start_at": "09:00",
      "end_at": "18:00",
      "is_day_of": "Флаг выходного дня",
      "description": "Только прием документов"
    }
  ],
  "problem_categories": [
    {
      "id": 1,
      "title": "Яма на дороге",
      "mnemonic_name": "yama_na_doroge",
      "hash_tag": "#дорожное_движение",
      "icon": "https://test.com/123.jpg",
      "rating": 10,
      "is_active": true,
      "is_visible": true,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "is_active": true,
  "generate_daily_report": true,
  "need_inform_by_email": true,
  "need_inform_by_sms": true,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```

#### **DELETE /contractors/(id)**
##### **Удалить исполнительного органа по ID**

(МОЖЕТ ТОЛЬКО АДМИН)

Response result 200
```JSON
{
  "id": 1,
  "mnemonic_name": "mvd",
  "title": "Министерство внутренних дел",
  "description": "Министерство внутренних дел - контролирующий орган",
  "responsible_person": "Петров В.В., старший лейтинант",
  "image": "avatar.jpg",
  "hash_tag": "#мвд",
  "contact_phone": "0713333333",
  "contact_email": "mvd@mvd.com",
  "pre_controller_email": "mvd@mvd.com",
  "telegram_chat_id": "-10000000001",
  "public_website": "https://mvd.com",
  "more_info": "На службе добра",
  "type": "EXECUTIVE",
  "schedule": [
    {
      "title": "Понедельник",
      "day_index": "1",
      "start_at": "09:00",
      "end_at": "18:00",
      "is_day_of": "Флаг выходного дня",
      "description": "Только прием документов"
    }
  ],
  "problem_categories": [
    {
      "id": 1,
      "title": "Яма на дороге",
      "mnemonic_name": "yama_na_doroge",
      "hash_tag": "#дорожное_движение",
      "icon": "https://test.com/123.jpg",
      "rating": 10,
      "is_active": true,
      "is_visible": true,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "is_active": true,
  "generate_daily_report": true,
  "need_inform_by_email": true,
  "need_inform_by_sms": true,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```

#### **POST /contractors**
##### **Создать нового исолнительного органа**

(МОЖЕТ ТОЛЬКО АДМИН)

Request body
```JSON
{
  "mnemonic_name": "mvd",
  "title": "Министерство внутренних дел",
  "description": "Министерство внутренних дел - контролирующий орган",
  "responsible_person": "Петров В.В., старший лейтинант",
  "image": "avatar.jpg",
  "hash_tag": "#мвд",
  "contact_phone": "0713333333",
  "contact_email": "mvd@mvd.com",
  "pre_controller_email": "mvd@mvd.com",
  "telegram_chat_id": "-10000000001",
  "public_website": "https://mvd.com",
  "more_info": "На службе добра",
  "type": "EXECUTIVE",
  "schedule": [],
  "problem_categories": [
    1,
    2,
    3,
    4
  ],
  "is_active": true,
  "generate_daily_report": true,
  "need_inform_by_email": true,
  "need_inform_by_sms": true
}
```

Response result 200
```JSON
{
  "id": 1,
  "mnemonic_name": "mvd",
  "title": "Министерство внутренних дел",
  "description": "Министерство внутренних дел - контролирующий орган",
  "responsible_person": "Петров В.В., старший лейтинант",
  "image": "avatar.jpg",
  "hash_tag": "#мвд",
  "contact_phone": "0713333333",
  "contact_email": "mvd@mvd.com",
  "pre_controller_email": "mvd@mvd.com",
  "telegram_chat_id": "-10000000001",
  "public_website": "https://mvd.com",
  "more_info": "На службе добра",
  "type": "EXECUTIVE",
  "schedule": [
    {
      "title": "Понедельник",
      "day_index": "1",
      "start_at": "09:00",
      "end_at": "18:00",
      "is_day_of": "Флаг выходного дня",
      "description": "Только прием документов"
    }
  ],
  "problem_categories": [
    {
      "id": 1,
      "title": "Яма на дороге",
      "mnemonic_name": "yama_na_doroge",
      "hash_tag": "#дорожное_движение",
      "icon": "https://test.com/123.jpg",
      "rating": 10,
      "is_active": true,
      "is_visible": true,
      "deleted_at": "2022-01-01 12:00:00",
      "created_at": "2022-01-01 12:00:00",
      "updated_at": "2022-01-01 12:00:00"
    }
  ],
  "is_active": true,
  "generate_daily_report": true,
  "need_inform_by_email": true,
  "need_inform_by_sms": true,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```

### **Категории проблем**
#### **GET /problem-categories**
##### **Списки категорий проблем**

url params:

page - (integer) номер страницы результата.
size - (integer) количество выводимых записей результата на страницу.

Response result 200
```JSON
{
  "links": {
    "first": "http://localhost:8000/api/{method_name}?page=1",
    "last": "http://localhost:8000/api/{method_name}?page=1",
    "prev": "http://localhost:8000/api/{method_name}?page=1",
    "next": "http://localhost:8000/api/{method_name}?page=1"
  },
  "current_page": 1,
  "from": 1,
  "last_page": 1,
  "path": "http://localhost:8000/api/{method_name}",
  "per_page": 30,
  "to": 1,
  "total": 10,
  "data": [
    {
        "id": 1,
        "title": "Яма на дороге",
        "mnemonic_name": "yama_na_doroge",
        "hash_tag": "#дорожное_движение",
        "icon": "https://test.com/123.jpg",
        "rating": 10,
        "is_active": true,
        "is_visible": true,
        "deleted_at": "2022-01-01 12:00:00",
        "created_at": "2022-01-01 12:00:00",
        "updated_at": "2022-01-01 12:00:00"
    }
  ]
```

#### **GET /problem-categories/(id)**
##### **Получить категорию проблем по ID**

Response result 200
```JSON
{
  "id": 1,
  "title": "Яма на дороге",
  "mnemonic_name": "yama_na_doroge",
  "hash_tag": "#дорожное_движение",
  "icon": "https://test.com/123.jpg",
  "rating": 10,
  "is_active": true,
  "is_visible": true,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```
#### **PUT /problem-categories/(id) (token required)**
##### **Редактировать категорию проблем пользователя по ID**

(МОЖЕТ ТОЛЬКО АДМИН)

Request body
```JSON
{
  "title": "Яма на дороге",
  "mnemonic_name": "yama_na_doroge",
  "hash_tag": "#дорожное_движение",
  "icon": "https://test.com/123.jpg",
  "rating": 10,
  "is_active": true,
  "is_visible": true
}
```

Response result 200
```JSON
{
  "id": 1,
  "title": "Яма на дороге",
  "mnemonic_name": "yama_na_doroge",
  "hash_tag": "#дорожное_движение",
  "icon": "https://test.com/123.jpg",
  "rating": 10,
  "is_active": true,
  "is_visible": true,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```

#### **DELETE /problem-categories/(id) (token required)**
##### **Удалить категорию проблем по ID**

(МОЖЕТ ТОЛЬКО АДМИН)

Response result 200
```JSON
{
  "id": 1,
  "title": "Яма на дороге",
  "mnemonic_name": "yama_na_doroge",
  "hash_tag": "#дорожное_движение",
  "icon": "https://test.com/123.jpg",
  "rating": 10,
  "is_active": true,
  "is_visible": true,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```

#### **POST /problem-categories (token required)**
##### **Создать категорию проблем**
(МОЖЕТ ТОЛЬКО АДМИН)

Request body
```JSON
{
  "title": "Яма на дороге",
  "mnemonic_name": "yama_na_doroge",
  "hash_tag": "#дорожное_движение",
  "icon": "https://test.com/123.jpg",
  "rating": 10,
  "is_active": true,
  "is_visible": true
}
```

Response result 200
```JSON
{
  "id": 1,
  "title": "Яма на дороге",
  "mnemonic_name": "yama_na_doroge",
  "hash_tag": "#дорожное_движение",
  "icon": "https://test.com/123.jpg",
  "rating": 10,
  "is_active": true,
  "is_visible": true,
  "deleted_at": "2022-01-01 12:00:00",
  "created_at": "2022-01-01 12:00:00",
  "updated_at": "2022-01-01 12:00:00"
}
```
#### **GET /problem-categories/(id)/active-requests**
##### **Списки активных заявок категорий проблем по ID**

url params:

page - (integer) номер страницы результата.
size - (integer) количество выводимых записей результата на страницу.

Response result 200
```JSON
{
  "links": {
    "first": "http://localhost:8000/api/{method_name}?page=1",
    "last": "http://localhost:8000/api/{method_name}?page=1",
    "prev": "http://localhost:8000/api/{method_name}?page=1",
    "next": "http://localhost:8000/api/{method_name}?page=1"
  },
  "current_page": 1,
  "from": 1,
  "last_page": 1,
  "path": "http://localhost:8000/api/{method_name}",
  "per_page": 30,
  "to": 1,
  "total": 10,
  "data": [
    {
        "id": 1,
        "title": "Яма на дороге",
        "mnemonic_name": "yama_na_doroge",
        "hash_tag": "#дорожное_движение",
        "icon": "https://test.com/123.jpg",
        "rating": 10,
        "is_active": true,
        "is_visible": true,
        "deleted_at": "2022-01-01 12:00:00",
        "created_at": "2022-01-01 12:00:00",
        "updated_at": "2022-01-01 12:00:00"
    }
  ]
```

#### **GET /problem-categories/(id)/archive-requests**
##### **Списки архивных заявок категорий проблем по ID**

url params:

page - (integer) номер страницы результата.
size - (integer) количество выводимых записей результата на страницу.

Response result 200
```JSON
{
  "links": {
    "first": "http://localhost:8000/api/{method_name}?page=1",
    "last": "http://localhost:8000/api/{method_name}?page=1",
    "prev": "http://localhost:8000/api/{method_name}?page=1",
    "next": "http://localhost:8000/api/{method_name}?page=1"
  },
  "current_page": 1,
  "from": 1,
  "last_page": 1,
  "path": "http://localhost:8000/api/{method_name}",
  "per_page": 30,
  "to": 1,
  "total": 10,
  "data": [
    {
        "id": 1,
        "title": "Яма на дороге",
        "mnemonic_name": "yama_na_doroge",
        "hash_tag": "#дорожное_движение",
        "icon": "https://test.com/123.jpg",
        "rating": 10,
        "is_active": true,
        "is_visible": true,
        "deleted_at": "2022-01-01 12:00:00",
        "created_at": "2022-01-01 12:00:00",
        "updated_at": "2022-01-01 12:00:00"
    }
  ]
```

#### **GET /problem-categories/(id)/completed-requests**
##### **Списки выполненных заявок категорий проблем по ID**

url params:

page - (integer) номер страницы результата.
size - (integer) количество выводимых записей результата на страницу.

Response result 200
```JSON
{
  "links": {
    "first": "http://localhost:8000/api/{method_name}?page=1",
    "last": "http://localhost:8000/api/{method_name}?page=1",
    "prev": "http://localhost:8000/api/{method_name}?page=1",
    "next": "http://localhost:8000/api/{method_name}?page=1"
  },
  "current_page": 1,
  "from": 1,
  "last_page": 1,
  "path": "http://localhost:8000/api/{method_name}",
  "per_page": 30,
  "to": 1,
  "total": 10,
  "data": [
    {
        "id": 1,
        "title": "Яма на дороге",
        "mnemonic_name": "yama_na_doroge",
        "hash_tag": "#дорожное_движение",
        "icon": "https://test.com/123.jpg",
        "rating": 10,
        "is_active": true,
        "is_visible": true,
        "deleted_at": "2022-01-01 12:00:00",
        "created_at": "2022-01-01 12:00:00",
        "updated_at": "2022-01-01 12:00:00"
    }
  ]
```