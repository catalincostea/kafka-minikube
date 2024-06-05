FROM python:3.8-slim
WORKDIR /app
COPY consumer_health_check_service.py /app
RUN pip install flask confluent_kafka
CMD ["python", "consumer_health_check_service.py"]
