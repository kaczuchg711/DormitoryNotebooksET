FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get install libmariadb-dev-compat
RUN pip install -r requirements.txt
COPY . /code/