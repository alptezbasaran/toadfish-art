FROM python:3.11-slim

RUN pip install --no-cache-dir \
    scipy \
    numpy \
    matplotlib \
    soundfile

WORKDIR /app
