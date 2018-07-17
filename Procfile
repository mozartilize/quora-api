release: poetry install --no-dev
release: cd src/ && poetry run flask db upgrade
web: uwsgi uwsgi.ini
