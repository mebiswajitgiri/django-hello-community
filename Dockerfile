FROM python:3.10.12-bullseye
ENV PYTHONUNBUFFERED 1
RUN mkdir /django
WORKDIR /django
COPY ./mssql-django-requirement.txt .
RUN pip install -r mssql-django-requirement.txt
COPY . .
EXPOSE 3000
