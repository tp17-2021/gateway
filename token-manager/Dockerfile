FROM python:3.10 as base

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apt-get update
RUN apt-get install netcat -y

RUN pip install --upgrade -r /code/requirements.txt

COPY ./src /code/src

FROM base as test
COPY ./test.py /code/test.py
COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "./start_test.sh" ]

FROM base as build
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80" ]
