FROM python:3

RUN mkdir /django-website
WORKDIR /django-website
COPY . /django-website
RUN pip install -r requirements.txt