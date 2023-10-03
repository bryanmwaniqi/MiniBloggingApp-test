FROM python:3.6-alpine

WORKDIR /app

COPY . /app/

ENV FLASK_APP=run.py FLASK_RUN_HOST=0.0.0.0


RUN pip install -r requirements.txt

CMD ["flask", "run"]