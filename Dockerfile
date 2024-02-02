FROM python:3.12-alpine3.19
WORKDIR /usr/gabduel
ENV FLASK_DEBUG 1
ENV fLASK_APP app.py
ENV APP_ENV development
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ ./
RUN python create_db_data.py
EXPOSE 5000
CMD ["python","-m","flask","run","--host=0.0.0.0"]
