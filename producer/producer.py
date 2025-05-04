import json
import time
# import uuid
import random
from kafka import KafkaProducer

from users_list import users

KAFKA_SERVER = 'kafka:9092'
TOPIC = 'clicks'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_event():
    return {
        'user_id': random.choice(users),
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        'page': '/home'
    }

if __name__ == '__main__':
    print('Xx'*80)
    print("Starting producer...")
    print('Xx'*80)
    # time.sleep(15)  # done in Dockerfile: CMD ["sh", "-c", "sleep 10 && python /app/producer.py"]
    counter = 0
    while True:
        event = generate_event()
        producer.send(TOPIC, event)
        print(f' {counter} Produced: {event}')
        counter += 1
        time.sleep(1)
