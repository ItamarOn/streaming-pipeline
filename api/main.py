from fastapi import FastAPI, HTTPException
import redis

app = FastAPI()

# Redis connection
r = redis.Redis(host="redis", port=6379, decode_responses=True)

@app.get("/clicks/{user_id}")
def get_click_count(user_id: str):
    count = r.hget("clicks", user_id)
    if count is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "click_count": int(count)}