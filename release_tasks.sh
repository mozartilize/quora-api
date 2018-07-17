#!/bin/bash

cd src/ && \
poetry install --no-dev -E deploy && \
poetry run flask db upgrade
