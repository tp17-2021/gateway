FROM python:3.10 as base

WORKDIR /code

# RUN apk add -U bash libusb-dev
RUN apt-get update
RUN apt-get install -y libusb-dev netcat

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade -r /code/requirements.txt

COPY ./src /code/src

FROM base as test
COPY ./test.py /code/test.py
COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "./start_test.sh" ]

FROM base as build
CMD [ "python3", "src/main.py" ]
