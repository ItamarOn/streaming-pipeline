FROM python:3.10-slim

WORKDIR /app

COPY producer.py .
COPY users_list.py .

RUN pip install kafka-python

CMD ["sh", "-c", "sleep 10 && python /app/producer.py"]