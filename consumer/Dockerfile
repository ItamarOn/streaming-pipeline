FROM python:3.10-slim

WORKDIR /app

COPY consumer.py .

RUN pip install kafka-python redis

CMD ["sh", "-c", "sleep 10 && python /app/consumer.py"]