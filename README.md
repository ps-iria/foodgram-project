[![foodgram workflow](https://github.com/ps-iria/foodgram-project/actions/workflows/main.yml/badge.svg)](https://github.com/ps-iria/foodgram-project/actions/workflows/main.yml)

# **«Продуктовый помощник»**
***
Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

***


## Установка проекта (на примере Linux)

- Создайте папку для проекта foodgram `mkdir foodgram` и перейдите в нее `cd foodgram`
- Склонируйте этот репозиторий в текущую папку `git clone https://github.com/ps-iria/foodgram-project `.
- Запустите docker-compose `sudo docker-compose up -d` 
- Примените миграции `sudo docker-compose exec web python manage.py migrate`
- Соберите статику `sudo docker-compose exec web python manage.py collectstatic --no-input`
- Создайте суперпользователя Django `sudo docker-compose exec web python manage.py createsuperuser`

## Тестирование

Для локального тестирования можно загрузить данные из фикстур 
```sh
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

***
## **Технологии**
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Nginx](https://nginx.org/)
- [Gunicorn](https://gunicorn.org/)
- [Docker](https://www.docker.com/)
- [Яндекс Облако](https://cloud.yandex.ru/)
- [GitHub Actions](https://github.com/features/actions)
