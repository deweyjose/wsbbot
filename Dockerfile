FROM python:3.7-alpine

WORKDIR /wsbbot-api

COPY requirements.txt .

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY controller ./api
COPY core ./core
COPY model ./model
COPY tools ./tools
COPY migrations ./migrations
COPY test ./test
COPY main.py ./

ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:5000 --workers=4 --keep-alive=60 --access-logfile=-"
CMD ["gunicorn", "main:app"]