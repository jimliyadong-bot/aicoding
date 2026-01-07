"""
Redis 连接管理
"""
from typing import Optional
import redis.asyncio as aioredis
from app.core.config import settings


class RedisClient:
    """Redis 客户端"""
    
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
    
    async def connect(self):
        """连接 Redis"""
        self.redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            encoding="utf-8",
            decode_responses=True
        )
    
    async def close(self):
        """关闭连接"""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> Optional[str]:
        """获取值"""
        if self.redis:
            return await self.redis.get(key)
        return None
    
    async def set(self, key: str, value: str, expire: int = None):
        """设置值"""
        if self.redis:
            await self.redis.set(key, value, ex=expire)
    
    async def setex(self, key: str, seconds: int, value: str):
        """设置值并指定过期时间(秒)"""
        if self.redis:
            await self.redis.setex(key, seconds, value)
    
    async def delete(self, key: str):
        """删除键"""
        if self.redis:
            await self.redis.delete(key)

    
    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if self.redis:
            return await self.redis.exists(key) > 0
        return False


# 全局 Redis 客户端实例
redis_client = RedisClient()


async def get_redis() -> RedisClient:
    """获取 Redis 客户端"""
    return redis_client
