from flask import Flask, jsonify, request
from confluent_kafka import Producer
import json
import datetime
import os
import threading
import time

app = Flask(__name__)

# Kafka producer configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092'
}
# producer_config['bootstrap.servers'] = 'kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092'
producer_config['bootstrap.servers'] = os.getenv("KAFKA_BOOTSTRAP_PRODUCERS")


producer = Producer(producer_config)

def produce_health_check():
    while True:
        health_check = {
            "service_name": "MyService",
            "status": "OK",
            "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
        }
        producer.produce('health_checks_topic', json.dumps(health_check).encode('utf-8'))
        producer.flush()
        time.sleep(60)  # Perform health check every 60 seconds

@app.route('/check_health', methods=['GET'])
def check_health():
    health_check = {
        "service_name": "MyService",
        "status": "OK",
        "timestamp": datetime.datetime.utcnow().isoformat() + 'Z'
    }
    producer.produce('health_checks_topic', json.dumps(health_check).encode('utf-8'))
    producer.flush()
    app.logger.info(f"Health check sent: {health_check}")
    return jsonify(health_check)

if __name__ == '__main__':
    threading.Thread(target=produce_health_check).start()
    app.run(host='0.0.0.0', port=5000)
