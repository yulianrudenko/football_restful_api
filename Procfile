release: python src/manage.py makemigrations && python src/manage.py migrate
web: daphne src.core.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=core.settings.production -v2