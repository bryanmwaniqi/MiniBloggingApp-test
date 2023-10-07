FROM python:3.6-alpine

WORKDIR /app

ENV FLASK_APP=run.py FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt .

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . /app

CMD ["flask", "run"]