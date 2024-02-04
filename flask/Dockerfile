FROM python:3.12-alpine3.19

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

# This connects to a database called db
ENV DATABASE_URL postgresql://postgres:postgres@db:5432/gabduel
ENV APP_ENV production
EXPOSE 5000
# Uses gunicorn instead of flask built-in server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
