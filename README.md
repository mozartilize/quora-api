# Requirements
- Python 3.6
- Poetry
- Docker


# Setup
1. Install packages:

```bash
../src$ poetry install
```


2. Create database service

```bash
docker service create \
--name quoradb \
--mount type=volume,source=quoradb,destination=/var/lib/postgresql/data \
-p 5001:5432 \
-e POSTGRES_PASSWORD=quora \
-e POSTGRES_USER=quora \
-e POSTGRES_DB=quora_development postgres:9.6
```


# Run

```bash
../src$ FLASK_ENV=development flask run
```


# Application structure

This project is where I try something new about SQLAlchemy core, that means there is no more ORM.

- tables/ contains all table definitions. Any change will be detected by Alembic for migrations.
- repository/ is where queries executed and data retrieved
- schemas/ is where user input data validated and data serialization

### Flows

`users post data ---> endpoints ---> (schemas, repository) ---> database(tables)`

`users request resources ---> endpoints ---> (repository, schemas) ---> return resources`


# Guideline

This project uses pylint and editorconfig for coding style check
