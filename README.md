# Телеграмм-бот для игры в "Блэкджек"

## Технический стек

![](https://img.shields.io/badge/-Python-386e9d?style=for-the-badge&logo=Python&logoColor=ffd241&) ![](https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white) ![](https://img.shields.io/badge/rabbitmq-%23FF6600.svg?&style=for-the-badge&logo=rabbitmq&logoColor=white) ![](https://img.shields.io/badge/-Aiohttp-DCDCDC?style=for-the-badge&logo=Aiohttp&logoColor=blue) ![](https://img.shields.io/badge/-sqlalchemy-4479A7?style=for-the-badge&amp;&amp;logoColor=ffffff) ![](https://img.shields.io/badge/-Postgresql-%232c3e50?style=for-the-badge&logo=Postgresql) ![](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## Реализовано:
1. Бот с полноценным геймплеем и защитой от спама (троттлингом).
2. Отдельный сервис для пуллинга Telegram-API с RabbitMQ.
3. Сервис API для администратора.
4. Авто-деплой на удаленный сервер и загрузка образа в registry с помощью Github-Actions.

## Архитектура:
Монолит
Разделение на слои:
- core (entities + usercases)
- adapters(infrastructure +presentation)
В ядре находятся обработчики бизнес логики, модели предметной области и протоколы, которые реализованы на слое adapters. 
Такой подход дает удобство тестирования, и уменьшения зависимостей от реализаций.

## Запуск

### В докер-контейнерах.
1. Клонировать репозиторий.
```
~$ git clone https://github.com/DeNeMiX83/black_jack
```
2. Создать .env в директории deploy на примере .env.example и экспортировать ENV. **_НЕ ЗАБУДЬТЕ ПОМЕНЯТЬ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ НА СВОИ!!!_**
```
~$ cd deploy && mv .env.dev.example .env.dev && export ENV=1
```
3. Собрать контейнеры.
```
~$ make compose-build
```
4. Поднять контейнеры.
```
~$ make compose-up
```

### На сервере с помощью github-actions.
1. Нужно конфигурировать секреты (крененшиалы для сервера) в github-secrets, необходимые секреты:
   - SERVER_USER
   - SERVER_IP
   - SERVER_SSH_KEY
   - SERVER_SSH_PORT

3. Создать директорию с проектом, в нем создать директорию  deploy со следующим содержимым:
   - docker-compose.yml
   - .env
   - alembic.ini

5. Cоздать файл prestart.sh в домашней директории.
   Пример содержимого
   ```
   cd /home/user/code/black_jack
   make compose-down
   make compose-pull
   make compose-up
   ```
   
Активация экшена происходит через пуш коммита и ручной вызов через GUI в github.