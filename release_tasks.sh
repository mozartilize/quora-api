#!/bin/bash

poetry config settings.virtualenvs.create false

cd src/ && \
poetry install --no-dev && \
flask db upgrade
