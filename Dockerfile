FROM python:3-slim

ADD . /data
WORKDIR /data

ENV ENV production
ENV SECRET abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "app.py"]

