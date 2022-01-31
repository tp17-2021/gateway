FROM python:3.10-alpine as base

WORKDIR /code

RUN apk add -U g++ gcc git bash

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./rsaelectie-install.sh ./rsaelectie-install.sh

RUN ./rsaelectie-install.sh

COPY ./src /code/src

COPY ./test.py /code/test.py


FROM base as test
CMD ["pytest", "test.py", "-rP", "--verbose"]
# docker-compose -f docker-compose-test.yml build && docker-compose -f docker-compose-test.yml run --rm tests
# docker-compose -f docker-compose-test.yml stop; docker-compose -f docker-compose-test.yml rm -f; docker-compose -f docker-compose-test.yml build; docker-compose -f docker-compose-test.yml run --rm tests

FROM base as build
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80" ]
