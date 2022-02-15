FROM python:3.10-alpine as base

WORKDIR /code

RUN apk add -U g++ gcc git bash

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src


FROM base as test

COPY ./test.py /code/test.py
COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "./start_test.sh" ]
# docker-compose -f docker-compose.test.yml -f docker-compose.test.synchronization-service.yml -p g-test up --build --exit-code-from synchronization-service --force-recreate --remove-orphans

FROM base as build
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80" ]
