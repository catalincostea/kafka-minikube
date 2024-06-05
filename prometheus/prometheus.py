from prometheus_client import start_http_server, Counter
import time

REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')

def process_request():
    REQUESTS.inc()
    time.sleep(0.5)

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        process_request()
