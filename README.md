# Requirements:
- Python 3.6
- Pipenv
- Docker


# Setup:
1. Install packages:

```bash
../src$ pipenv install --ignore-pipfile --dev
```


2. Create database service

```bash
docker service create \
--name quoradb \
--mount type=volume,source=quoradb,destination=/var/lib/postgresql/data \
-e POSTGRES_PASSWORD=quora \
-e POSTGRES_USER=quora \
-e POSTGRES_DB=quora_development postgres:9.6
```


# Run:

```bash
../src$ FLASK_ENV=development flask run
```
