FROM ubuntu:22.04 AS base

WORKDIR /code

RUN apt update

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Bratislava

# RUN apt install -yq g++ gcc bash libffi-dev pip pandoc weasyprint netcat
RUN apt-get update && apt-get install -yq g++ gcc bash libffi-dev pip netcat wget xfonts-75dpi
RUN apt-get update && apt-get install -y coreutils apt-utils pandoc texlive-latex-base build-essential xorg libssl-dev libxrender-dev wget gdebi xvfb libfontconfig wkhtmltopdf

COPY ./requirements.txt ./code/requirements.txt

RUN pip3 install --upgrade pip

RUN pip3 install --upgrade -r ./code/requirements.txt

COPY ./src /code/src

COPY ./config.json ./code/config.json

FROM base as test

COPY ./tests /code/tests
COPY ./start_test.sh ./start_test.sh
RUN chmod 700 ./start_test.sh
CMD [ "./start_test.sh" ]


FROM base as build

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80" ]
