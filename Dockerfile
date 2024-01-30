FROM python:3.12-alpine3.19
WORKDIR /docker_app
COPY . /docker_app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","-m","flask","run","--host=0.0.0.0"]
