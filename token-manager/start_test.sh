#!/bin/sh

while ! nc -z web 80; do
    echo "Waiting for the web server to start...";
    sleep 3;
done;

while ! nc -z statevector 80; do
    echo "Waiting for the statevector to start...";
    sleep 3;
done;

pytest -rP --verbose --disable-pytest-warnings
