# 🛠 Educational project
Online cinema. API can give information about movies in the database and about each specific movie or person, the application has an admin panel and full text search based on Elasticsearch which loads by ETL process.

The following tools were used in the backend part of the project:
- Python 3.10
- Django 3.2
- Elasticsearch 7.7
- Redis 6
- FastAPI

The infrastructure part used:
- PostgreSQL
- Docker
- Nginx


# 🚀 Project installation

Install Docker and docker-compose:
```sh
sudo apt-get update
sudo apt install docker.io 
sudo apt-get install docker-compose-plugin
```
Clone repository:
```sh
git clone git@github.com:gufin/Async_API_sprint_1.git
```
When deploying to a server, you need to create a file with the values of the .env variables in the docker_compose folder.
```sh
source Makefile env_file
```
When running on a server, you need to add the address of your server to the ALLOWED_HOSTS variable in the backend/foodgram/settings.py file.

##### 🐳 Running Docker containers
When you first start from the docker_compose directory, you need to run the command:
```sh
source Makefile full_run
```
On subsequent launches, the --build key can omit.

Create django superuser:
```sh
sudo docker-compose exec web python manage.py createsuperuser
```

[Admin panel](http://127.0.0.1:8000/admin/) 

[ElasticSearch API](http://127.0.0.1:9200) 

[FastApi documentation](http://localhost:8001/api/openapi/) 

##### Linked projects
[ETL](https://github.com/agatma/new_admin_panel_sprint_3) 

# :smirk_cat: Authors
Drobyshev Ivan

[Agatanov Madihan](https://github.com/agatma/) 

