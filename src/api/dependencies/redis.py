from redis.asyncio import Redis
from starlette.requests import Request


def get_redis_connection(request: Request) -> Redis:
    return request.app.state.redis
