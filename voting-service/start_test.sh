#!/bin/bash

while ! nc -z web 80; do
    echo "Waiting for the web server to start...";
    sleep 3;
done;

# generate python vote class from json spec
datamodel-codegen --url http://web/statevector/config/datamodels.yaml --output /code/src/schemas.py

# run tests
pytest -srP --verbose --asyncio-mode=strict --disable-pytest-warnings
