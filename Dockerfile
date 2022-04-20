# pull official base image
FROM python:3.9.6

# set work directory
WORKDIR /podcast

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
#RUN apk update \
#    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
COPY Pipfile Pipfile.lock /podcast/
RUN pip install pipenv && pipenv install --system
#RUN groupadd -r app && useradd --system app -g app \
#    && chown -R app:app /podcast && chmod -R 755 /podcast \
#    && chown -R app:app /usr/local/lib/python3.9/site-packages \
#    && chmod -R 755 /usr/local/lib/python3.9/site-packages

# copy project
COPY . /podcast/
#USER app