FROM python:3.9.7-alpine3.14

RUN apk update && \
    apk add --no-cache --virtual \
        build-deps \
        gcc \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        musl-dev

WORKDIR /crawler

COPY ./crawler/requirements.txt .

RUN pip install -r requirements.txt

COPY ./crawler .
