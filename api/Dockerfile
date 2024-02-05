FROM python:3.12-alpine3.19

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

# This connects to a database called db
ENV DATABASE_URL postgresql://postgres:postgres@db:5432/gabduel
ENV APP_ENV production

# For elastic beanstalk only for nginx. Actually runs on port 5000
EXPOSE 80

# Uses gunicorn instead of flask built-in server
CMD ["gunicorn", "--workers", "3", "--threads", "12", "--preload", "--bind", "0.0.0.0:5000", "wsgi:app"]
