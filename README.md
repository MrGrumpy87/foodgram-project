# foodgram-project
%foodgram-project%

## Необходимые инструменты
* [pip](https://pypi.org/project/pip/)
* [pip-tools](https://github.com/jazzband/pip-tools)
* [virtual env](https://docs.python.org/3/library/venv.html)
* [pdfkit](https://pypi.org/project/pdfkit/)

## Установка и запуск проекта
Для запуска приложения необходимо:
1. Активировать виртуальное окружение
2. Установить зависимости
   ```shell
   pip install -r requirements.txt
   ```
3.  Применить миграции к БД
    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```
4. Создать суперпоьзователя
   ```shell
   python manage.py createsuperuser
   ```
5. Заполнить БД предварительными данными
   * ингредиенты
        ```shell
        python manage.py loaddata ingredients.json
        ```
   * тэги
        ```shell
        python manage.py loaddata tags.json
        ```
6. Собрать статику
   ```shell
   python manage.py collectstatic
   ```
7. Запустить приложение
   ```shell
   python manage.py runserver
   ```