PROJECT_NAME = Movies

all:
	@echo "make env_file		- Создать .env file на основе .env_example. - СДЕЛАЙТЕ ПЕРВЫМ ДЕЙСТВИЕМ"
	@echo "make full_run		- Запуск контейнеров с миграциями и бекапом."
	@echo "make etl_logs		- Посмотреть логи ETL сервиса."
	@echo "make run		- Пустой запуск контейнеров (не рекомендуется)."
	@echo "make superuser		- Создать суперпользователя "
	@echo "make migrate		- Выполнить миграции "
	@echo "make load		- Загрузить данные в postgresql "
	@echo "make django_admin	- Консоль django контейнера."
	@echo "make etl		- Консоль ETL контейнера."
	@echo "make postgresql		- Консоль postgresql контейнера."
	@echo "make nginx		- Консоль nginx контейнера."
	@echo "make stop		- Остановка контейнеров."
	@echo "make stop_d		- Остановка контейнеров и удаление томов "

full_run:
	#docker-compose up Команда для сборки и запуска контейнеров.
	#--build Сборка образа перед запуском контейнера.
	#-d Detached mode.
	docker-compose up --build -d backend db nginx elasticsearch redis

	#Подключение к консоли веб-контейнера для создания миграций.
	docker-compose run backend python manage.py migrate

	#Подключение к консоли веб-контейнера для загрузки бэкапа в базу данных.
	docker-compose run backend python manage.py loaddata dump.json

	#Запуск ETL сервиса
	docker-compose up -d etl

	#Ожидаем загрузки документов в Elasticsearch
	sleep 5

	#Вывод результатов загрузки
	docker-compose exec etl  tail -n 300 cat logs/etl.log

    #Запуск FastAPI сервиса
	docker-compose up --build -d fastapi

	return 1

env_file:
	#Создание .env file на основе .env_example.
	cp .env-example .env

run:
    #docker-compose up Пустой запуск контейнеров (не рекомендуется)..
	#--build Сборка образа перед запуском контейнера.
	#-d Detached mode.
	docker-compose up --build -d

django_admin:
	#Запуск консоли для управления django-admin контейнером.
	docker-compose exec backend bash

etl_logs:
    #Посмотреть логи ETL сервиса.
	docker-compose exec etl  tail -n 300 cat logs/etl.log

etl:
    #Запуск консоли для управления ETL контейнером.
	docker-compose exec etl bash


postgresql:
	#Запуск консоли для управления Postgres контейнером.
	docker-compose exec db bash

nginx:
	#Запуск консоли для управления nginx контейнером.
	docker-compose exec nginx bash

stop:
	#Остановка контейнеров, запущенных docker-compose up.
	docker-compose down

stop_d:
	#Остановка контейнеров, запущенных docker-compose up и удаление томов.
	docker-compose down -v

migrate:
	#Подключение к консоли django-admin для создания миграций.
	docker-compose run backend python manage.py migrate

load:
	#Подключение к консоли django-admin для загрузки бэкапа в базу данных.
	docker-compose run backend python manage.py loaddata dump.json

superuser:
	#Подключение к консоли django-admin для создания Суперпользователя (администратор).
	docker-compose run backend python manage.py createsuperuser

