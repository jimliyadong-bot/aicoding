"""
Redis 客户端
"""
import redis.asyncio as redis
from app.core.config import settings


class RedisClient:
    """Redis 客户端"""
    
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        """连接 Redis"""
        self.redis = await redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
    
    async def close(self):
        """关闭连接"""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> str | None:
        """获取值"""
        if not self.redis:
            await self.connect()
        return await self.redis.get(key)
    
    async def set(self, key: str, value: str, ex: int | None = None):
        """设置值"""
        if not self.redis:
            await self.connect()
        await self.redis.set(key, value, ex=ex)
    
    async def incr(self, key: str) -> int:
        """自增"""
        if not self.redis:
            await self.connect()
        return await self.redis.incr(key)
    
    async def expire(self, key: str, seconds: int):
        """设置过期时间"""
        if not self.redis:
            await self.connect()
        await self.redis.expire(key, seconds)
    
    async def setex(self, key: str, seconds: int, value: str):
        """设置值并指定过期时间(秒)"""
        if not self.redis:
            await self.connect()
        await self.redis.setex(key, seconds, value)
    
    async def delete(self, key: str):
        """删除键"""
        if not self.redis:
            await self.connect()
        await self.redis.delete(key)



# 创建全局实例
redis_client = RedisClient()
