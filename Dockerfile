FROM python:3.8-alpine

# install pipenv, gcc, devel

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev\
    python3-dev \
    && pip install pipenv


WORKDIR /code/

ADD Pipfile* /code/
RUN pipenv sync
ADD . /code/
CMD ["pipenv", "run", "python", "handler.py"]
