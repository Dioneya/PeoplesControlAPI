# PeoplesControlAPI

Компоненты API для приложения "Народный Контроль". Данное API было разработано с помощью Python 3.8 и Flask 1.1.2.

## Установка API

1. Клонировать компоненты репозитория в удобное для вас место.
2. Создать вирутальное окружение с помощью virtualenv.
<pre>
    <code>
    virtualenv -p python3 envname
    </code>
</pre>
3. Затем необходимо перейти в созданное виртуальное окружение.
<pre>
    <code>
    source ./ИМЯ_ВИРТ_ОКРУЖЕНИЯ/bin/activate # пример для linux
    </code>
</pre>
4. Установить зависимости компонентов с помощью requirements.txt.
<pre>
    <code>
    pip3 install -r requirements.txt
    </code>
</pre>

5. Импортировать db.sql в базу данных MySQL.
6. Создать юзера для импортированной базы данных с возможность удаления/изменения/создание записей.
7. В файле api.py указать настройки подключения к базе данных в переменной "app.config['SQLALCHEMY_DATABASE_URI']"
<pre>
    <code>
    #./api.py

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://USER_NAME:PASSWORD@HOST/DATABESE_NAME'
    </code>
</pre>
7. В переменной DOMAIN_NAME файла api.py укажите текущее домен имя для корректного отобображения данных из некоторых роутов.
<pre>
    <code>
    #./api.py

    DOMAIN_NAME = "http://example_domain.com"
    </code>
</pre>
8. Для работы телеграм бота, необходимо в файле bot.py, расположенного в папке tg изменить переменную bot_token
<pre>
    <code>
    #./tg/bot.py

    bot_token = 'UR_BOT_TOKEN'
    </code>
</pre>

## Запуск API
1. Переходим в виртуально окружение
<pre>
    <code>
    source ./ИМЯ_ВИРТ_ОКРУЖЕНИЯ/bin/activate // пример для linux
    </code>
</pre>
2. Для дебага API, запуск осуществляется с помощью вызова файла api.py.
<pre>
    <code>
    python3 api.py
        или
    python api.py
    </code>
</pre>
===
Для запуска на хостинге рекомендуется запустить с помощью WSGI Gunicorn, предвартительно установив его на сервере.
<pre>
    <code>
    pip install gunicorn
    </code>
</pre>
Затем выполним запуск с помощью команды:
<pre>
    <code>
    gunicorn --bind адрес:порт api:app
    </code>
</pre>

## Список доступных роутов

#### GET /auth/login <span style="color:red;">token required</span>
