FROM python:3.8-slim
WORKDIR /app
COPY health_check_service.py /app
RUN pip install flask confluent_kafka
CMD ["python", "health_check_service.py"]
