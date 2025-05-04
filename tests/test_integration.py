import json
import time
import uuid
from kafka import KafkaProducer
import redis

def test_producer():
    # connection definition
    producer = KafkaProducer(bootstrap_servers="localhost:9092",
                             value_serializer=lambda v: json.dumps(v).encode("utf-8"))

    redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

    # produced sent message with user_id to Kafka
    user_id = str(uuid.uuid4())
    message = {
        "user_id": user_id,
        "timestamp": "2025-05-04T21:00:00Z",
        "page": "/test"
    }
    producer.send("clicks", value=message)
    producer.flush()

    # wait for the consumer to process the message
    time.sleep(2)

    # check in redis if the click count for the user_id is 1 - it's mean the consumer processed the message
    count = redis_client.get(user_id)
    print(f"User {user_id} click count: {count}")
    assert count == "1", f"Expected 1, got {count}"


def real_check_redis():
    r = redis.Redis(host="localhost", port=6379)
    raw = r.hgetall("clicks")
    data = {k.decode(): int(v.decode()) for k, v in raw.items()}
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    for i, (user, count) in enumerate(sorted_data[:10], 1):
        print(f"{i}. {user} - {count} clicks")
