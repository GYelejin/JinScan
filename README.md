# Сетевой сканер на языке Python

Это приложение представляет собой сетевой сканер на языке Python, который позволяет сканировать удаленные машины и получать информацию об операционной системе.

## Установка и запуск

Для запуска приложения необходимо выполнить следующие шаги:

Установить Python версии 3 и выше.

```bash
apt-get update && apt-get install -y python3 postgresql postgresql-contrib
```

Установить библиотеку Paramiko, psycopg2, Flask.

```bash
pip install psycopg2 flask paramiko
```

или

```bash
pip install -r requirements.txt
```

Скачать исходный код приложения.

```bash
git clone https://github.com/GYelejin/JinScan && cd JinScan
```

Отредактировать фаил .env.

```bash
# Database configuration
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=scannerapp
DB_USER=scannerapp
DB_PASSWORD=12345678
```


Создать базу данных PostgreSQL.

```bash
source .env
sudo systemctl start postgresql && \
sudo -u postgres psql -c "CREATE DATABASE ${POSTGRES_DB};" && \
sudo -u postgres psql -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${mysecretpassword}';" && \
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};"
```

Запустить приложение:

```bash
python app.py
```

## Функциональность

Приложение имеет следующую функциональность:

- Cканер системы на языке Python.
- Настройки сканирования в виде профиля, включающего логин, пароль, порт и IP-адрес.
- Подключения к машине по SSH и выполнения команд.
- Лог запущенных команд.
- Детектирование операционных систем Debian, Ubuntu, Manjaro и неизвестных дистрибутивов Linux.
- Поиск основных сведений об операционной системе (название, версия, архитектура).
- Запись данных в базу данных PostgreSQL.
- Веб-интерфейс для управления сканером.
