FROM python:3.10-alpine3.14 as base

WORKDIR /code

RUN apk add -U g++ gcc bash
RUN apk update && apk add tzdata
ENV TZ=Europe/Bratislava

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade -r /code/requirements.txt



FROM base as test

RUN pip install --no-cache-dir --upgrade pytest pytest-mock

COPY ./src /code/src
COPY ./tests /code/tests

COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "./start_test.sh" ]


FROM base as build

COPY ./src /code/src

COPY ./start_prod.sh ./start_prod.sh
RUN chmod 700 ./start_prod.sh
CMD [ "./start_prod.sh" ]
