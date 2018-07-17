release: cd src/ && poetry install --no-dev -E deploy
release: cd src/ && poetry run flask db upgrade
web: uwsgi uwsgi.ini
