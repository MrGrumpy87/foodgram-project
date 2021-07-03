# foodgram-project


## Необходимые инструменты
* [pip](https://pypi.org/project/pip/)
* [pip-tools](https://github.com/jazzband/pip-tools)
* [virtual env](https://docs.python.org/3/library/venv.html)
* [pdfkit](https://pypi.org/project/pdfkit/)
* [Docker](https://docs.docker.com/engine/install/)
* [Docker-Compose](https://docs.docker.com/compose/install/)

## Установка и запуск проекта
Для запуска проекта необходимо:
1. Устанавливаем Docker, Docker-Compose и [wkhtmltopdf](https://pypi.org/project/pdfkit/)
2. Создаем в корне проекта файл .env, в котором определяем переменные для подключения к БД PostgreSQL
```shell
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```
3. Собираем `docker-compose` в detach mode:
```shell
docker-compose up -d --build
```
4. Собираем статические файлы в `STATIC_ROOT`:
```shell
docker-compose exec web python manage.py collectstatic --noinput
```
5. Создаем и запускаем миграции:
```shell
docker-compose exec web python manage.py makemigrations --noinput
docker-compose exec web python manage.py migrate --noinput
```
6. Наполняем `Postgres` данными:
    * Ингредиенты
    ```shell
    docker-compose exec web python manage.py loaddata foodgram/fixtures/ingredients.json
    ```
   * Тэги
    ```shell
    docker-compose exec web python manage.py loaddata foodgram/fixtures/tags.json
    ```
7. Создаем суперпользователя Django:
```shell
docker-compose run web python manage.py createsuperuser
```