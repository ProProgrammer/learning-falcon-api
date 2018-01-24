FROM python:3.6-alpine3.7

RUN pip install -U pip
RUN pip install -U falcon redis

EXPOSE 8080
COPY . /falconratelimiter
WORKDIR /falconratelimiter

CMD ["python", "/falconratelimiter/app.py"]
