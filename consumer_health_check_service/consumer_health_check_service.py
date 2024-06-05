from flask import Flask, jsonify
from confluent_kafka import Consumer, KafkaException
import json
import os
import threading

app = Flask(__name__)

# Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'health_check_group',
    'auto.offset.reset': 'earliest'
}
# consumer_config['bootstrap.servers'] = 'kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092'
consumer_config['bootstrap.servers'] = os.getenv("KAFKA_BOOTSTRAP_CONSUMERS")

consumer = Consumer(consumer_config)
consumer.subscribe(['health_checks_topic'])

latest_health_check = {}

@app.route('/get_latest_health_check', methods=['GET'])
def get_latest_health_check():
    global latest_health_check
    return jsonify(latest_health_check)

def consume_health_check():
    global latest_health_check
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        latest_health_check = json.loads(msg.value().decode('utf-8'))
        app.logger.info(f"Consumed health check: {latest_health_check}")

if __name__ == '__main__':
    threading.Thread(target=consume_health_check).start()
    app.run(host='0.0.0.0', port=5001)
