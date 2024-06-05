FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install prometheus-client flask     # --no-cache-dir

EXPOSE 9090

CMD ["python", "prometheus.py"]
