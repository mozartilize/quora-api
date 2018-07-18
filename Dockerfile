FROM python:3.6

RUN pip install poetry

RUN poetry config settings.virtualenvs.create false

ADD src/ /app

WORKDIR /app

RUN poetry install --no-dev -E deploy

RUN useradd -m mark1
USER mark1

CMD ["uwsgi", "uwsgi.ini"]
