FROM python:3-slim

COPY app.py /data/
COPY config.py /data/
COPY core.py /data/
COPY requirements.txt /data/
WORKDIR /data

ENV ENV prod
ENV SECRET abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
ENV DOMAIN http://127.0.0.1:5000/

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "app.py"]
