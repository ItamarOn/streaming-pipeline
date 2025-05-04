import json
import os
# import time
from kafka import KafkaConsumer
from redis import Redis

KAFKA_TOPIC = 'clicks'
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

def main():
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='click-consumers',
    )

    print("Consumer started...")
    counter = 0
    for msg in consumer:
        user_id = msg.value.get("user_id")
        if user_id:
            r.hincrby("clicks", user_id, 1)
            print(f"{counter} Counted click for user {user_id}")
            counter += 1

if __name__ == "__main__":
    # time.sleep(10)  # in Dockerfile: CMD ["sh", "-c", "sleep 10 && python /app/consumer.py"]
    main()
