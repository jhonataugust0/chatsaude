# https://hub.docker.com/_/python
FROM python:3.9.16-slim

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./ 

EXPOSE 8000

RUN apt-get update 
RUN apt-get install -y postgresql libpq-dev python-dev python3-psycopg2 

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]