FROM python:3.10-alpine3.14 as base

WORKDIR /code

RUN apk add	-U bash libusb-dev

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src

FROM base as test
COPY ./test.py /code/test.py
COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "./start_test.sh" ]

FROM base as build
RUN apk add -U curl
COPY ./start_build.sh ./start_build.sh
RUN chmod 700 ./start_build.sh
CMD [ "./start_build.sh" ]