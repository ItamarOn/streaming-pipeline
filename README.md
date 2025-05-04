## streaming-pipeline

```
[Producer Pod] --> [Kafka] <-- [Consumer Pod] --> [Redis]   <-- [API Pod] <-- Client
```

### How to run
1. **Start Producer-Script, Kafka, Redis and Consumer**: 
   - Make sure you have Docker installed.
   - Run the following command to start Kafka:
     ```bash
     # docker-compose down
     docker-compose up -build
     ```
2. **Check there is data in redis**:
   - Run the following command to check if there is data in Redis:
     ```bash
     docker exec -it redis redis-cli
     ```
   - Then run the following command to check if there is data in Redis:
     ```bash
     keys *
     ```
   - or use python script to check if there is data in Redis:
     ```python
     import redis

     r = redis.Redis(host="localhost", port=6379)
     raw = r.hgetall("clicks")
     data = {k.decode(): int(v.decode()) for k, v in raw.items()}
     sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    
     for i, (user, count) in enumerate(sorted_data[:10], 1):
        print(f"{i}. {user} - {count} clicks")
     ```
    - This will print the top 10 users with the most clicks:
     ```
     1. matthew.thompson@dell.com - 38 clicks
     2. david.taylor@tesla.com - 37 clicks
     3. sophia.martin@cisco.com - 35 clicks
     4. nathan.scott@square.com - 34 clicks
    ```
3. **Start API**:
   -  GET `http://localhost:8000/clicks/emma.white@adobe.com` 
      returns:
   - ```json
     {
       "user_id":"emma.white@adobe.com",
       "clicks": 0
     }
     ```
