FROM python:3.11.3

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

#RUN apt-get update && apt-get upgrade -y && apt-get install postgresql gcc python3-dev musl-dev -y

RUN pip install --upgrade pip
COPY ./req.txt .
RUN pip install -r req.txt

COPY . .