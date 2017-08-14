FROM python:3.6.2-alpine3.6

COPY requirements.txt /src/requirements.txt
RUN apk add --no-cache \
        build-base \
        gcc \
        musl-dev \
        postgresql-dev \
        python3-dev && \
    python -m pip install --no-cache -r /src/requirements.txt

COPY . /src
CMD ["/usr/local/bin/python", "/src/server.py"]
