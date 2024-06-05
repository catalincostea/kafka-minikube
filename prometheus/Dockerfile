FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install prometheus-client

EXPOSE 8000

CMD ["python", "prometheus.py"]