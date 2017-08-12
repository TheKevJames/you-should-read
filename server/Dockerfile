FROM python:3.6.2-alpine3.6

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache -r requirements.txt

COPY . /src
CMD ['/src/server.py']
