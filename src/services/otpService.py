import random

import fastapi
from redis.asyncio import Redis


async def generate_otp(length: int = 6) -> str:
    """
    Generate a numeric OTP of specified length.
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


async def store_otp(redis: Redis, user_id: str, otp: str, expire_seconds: int = 300) -> None:
    """
    Store the OTP in Redis with an expiration time.
    """
    redis_conn = redis
    key = f"otp:{user_id}"
    await redis_conn.set(key, otp, ex=expire_seconds)


async def verify_otp(redis: Redis, user_id: str, otp: str) -> bool:
    """
    Verify the OTP provided by the user.
    """
    redis_conn = redis
    key = f"otp:{user_id}"
    stored_otp = await redis_conn.get(key)
    if stored_otp and stored_otp == otp:
        # Optionally, delete the OTP after verification to ensure it's used only once
        await redis_conn.delete(key)
        return True
    return False
