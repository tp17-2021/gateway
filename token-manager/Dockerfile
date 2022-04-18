FROM python:3.10 as base

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade -r /code/requirements.txt


FROM base as test

RUN apt-get update && apt-get install netcat -y
RUN pip install --no-cache-dir --upgrade pytest pytest-mock

COPY ./src /code/src
COPY ./tests /code/tests

COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "./start_test.sh" ]


FROM base as build

COPY ./src /code/src
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80" ]
