#!/bin/bash

while ! nc -z web 80; do
    echo "Waiting for the web server to start...";
    sleep 3;
done;

# generate python vote class from json spec
datamodel-codegen --url http://web/statevector/config/vote.json --output /code/src/schemas/vote.py

# start server
uvicorn src.main:app --host 0.0.0.0 --port 80
