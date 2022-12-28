FROM python:3.9.5-alpine

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh

COPY . /app/

RUN chmod +x docker-entrypoint.sh

CMD ["sh", "/app/docker-entrypoint.sh" ]