FROM python:3.8-alpine

# install pipenv, gcc, devel

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    cargo \
    && pip install pipenv \
    && apk del .build-deps

    
WORKDIR /code

ADD Pipfile* /code/
RUN pipenv sync
CMD ["pipenv", "run", "python", "handler.py"]
