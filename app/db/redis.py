from redis.asyncio import Redis
from app.config import settings

redis_client = Redis(
    host=settings.credentials.redis.host,
    port=settings.credentials.redis.port,
    password=settings.credentials.redis.password,
    decode_responses=True
)

async def get_redis():
    """Dependency helper jika nantinya ingin meng-inject Redis via FastAPI."""
    return redis_client