FROM python:3.10-alpine3.14 AS base

WORKDIR /code

COPY ./requirements.txt ./code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./code/requirements.txt

COPY ./src /code/src


FROM base as test
COPY ./tests /code/tests
CMD [ "pytest", "-srP", "--verbose", "--disable-pytest-warnings" ]


FROM base as build
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80" ]
