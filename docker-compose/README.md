# Реализация API для кинотеатра

Цель проекта: создать API, возвращающий список фильмов в формате, описанном в openapi-файле, и позволяющий получить информацию об одном фильме. Дополнительно реализован полнотекстовый поиск

### Перед запуском контейнеров создайте .env файл
```
make env_file
```

### Работа с проектом с помощью make
#### Список контейнеров: postgres, django-admin, elasticsearch, ETL-app, swagger, nginx

```
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
```
