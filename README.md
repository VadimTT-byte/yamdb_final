# yamdb_final
yamdb_final 
![yamdb_final workflow](https://github.com/VadimTT-byte/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# Проект: CI и CD проекта api_yamdb

Реализация веб-приложения api_yamdb и его развёртка через docker, docker-compose.

Дополнительно мы настроим CI и CD для возможности:
 
- автоматический запуск тестов,

- обновление образов на Docker Hub,

- автоматический деплой на боевой сервер при пуше в главную ветку main,

- получение уведомлений об успешном запуске в Telegram.


### Технологии
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-23.0.0-blue)](https://www.docker.com/)
![Docker-compose](https://img.shields.io/badge/Docker--compose-1.29.2-blue)


### Подготовка сервера
Установка docker и docker-compose:

- apt update && apt upgrade

- apt install docker.io

- apt install docker-compose-plugin
  
### Запуск проекта
Выполнить миграции

- docker-compose exec web python manage.py migrate

Создание superuser

- docker-compose exec web python manage.py createsuperuser

Собрать static

- docker-compose exec web python manage.py collectstatic --no-input

### После запуска, доступа документация для API, по адресу  

- http://158.160.16.197/redoc/


### Автор
[Вадим](https://github.com/VadimTT-byte)