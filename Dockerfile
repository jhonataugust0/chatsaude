# https://hub.docker.com/_/python
FROM python:3.9.16-slim

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV TZ='America/Sao_Paulo'

WORKDIR $APP_HOME

EXPOSE 8000

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y postgresql libpq-dev python-dev python3-psycopg2 

COPY . ./ 

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]