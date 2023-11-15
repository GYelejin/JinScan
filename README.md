# Сетевой сканер на языке Python

Это приложение представляет собой сетевой сканер на языке Python, который позволяет сканировать удаленные машины и получать информацию об операционной системе.

## Установка и запуск

Для запуска приложения необходимо выполнить следующие шаги:

Установить Python версии 3 и выше.

```bash
sudo apt-get update && sudo apt-get install -y git python3 python3-pip postgresql postgresql-contrib
```

Скачать исходный код приложения.

```bash
git clone https://github.com/GYelejin/JinScan && cd JinScan
```

Установить библиотеку Paramiko, psycopg2, Flask.

```bash
sudo apt-get install --reinstall libpq-dev
pip install jc psycopg2 flask paramiko python-dotenv
```

или

```bash
sudo apt-get install --reinstall libpq-dev
pip install -r requirements.txt
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
sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME};" && \
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';" && \
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"
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
