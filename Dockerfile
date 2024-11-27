FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www/src

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /var/www/src/
RUN pip install --upgrade pip setuptools \
    && pip install -r requirements.txt

COPY . /var/www/src/

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]