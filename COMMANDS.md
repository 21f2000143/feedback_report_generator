``poetry run python manage.py runserver
``poetry run celery -A config.celery worker -l info
``poetry run sudo service postgresql start
``poetry run sudo service redis-server start
``poetry run celery -A config.celery flower --port=5555