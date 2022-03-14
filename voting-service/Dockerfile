FROM python:3.10-alpine3.14 AS base

WORKDIR /code

RUN apk add -U g++ gcc bash

COPY ./requirements.txt ./code/requirements.txt

RUN pip install --upgrade -r ./code/requirements.txt

COPY ./src /code/src


FROM base as test

COPY ./tests /code/tests
COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "./start_test.sh" ]


FROM base as build

COPY ./start_prod.sh ./start_prod.sh
RUN chmod 700 ./start_prod.sh
CMD [ "./start_prod.sh" ]
