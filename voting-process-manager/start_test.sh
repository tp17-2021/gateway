#!/bin/bash

while ! nc -z web 80; do
    echo "Waiting for the web server to start...";
    sleep 3;
done;

# run tests
pytest -srP --verbose --asyncio-mode=strict --disable-pytest-warnings
