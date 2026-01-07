"""
登录限流工具
"""
from app.utils.redis_client import redis_client
from app.core.exceptions import TooManyRequestsException


async def check_login_limit(ip: str, username: str, max_attempts: int = 5, window: int = 300):
    """
    检查登录限流
    
    Args:
        ip: IP 地址
        username: 用户名
        max_attempts: 最大尝试次数
        window: 时间窗口(秒)
    
    Raises:
        TooManyRequestsException: 超过限流次数
    """
    # 检查 IP 限流
    ip_key = f"login_limit:ip:{ip}"
    ip_count = await redis_client.incr(ip_key)
    if ip_count == 1:
        await redis_client.expire(ip_key, window)
    if ip_count > max_attempts:
        raise TooManyRequestsException(f"登录次数过多,请 {window // 60} 分钟后再试")
    
    # 检查账号限流
    username_key = f"login_limit:username:{username}"
    username_count = await redis_client.incr(username_key)
    if username_count == 1:
        await redis_client.expire(username_key, window)
    if username_count > max_attempts:
        raise TooManyRequestsException(f"登录次数过多,请 {window // 60} 分钟后再试")


async def clear_login_limit(ip: str, username: str):
    """
    清除登录限流(登录成功后调用)
    
    Args:
        ip: IP 地址
        username: 用户名
    """
    ip_key = f"login_limit:ip:{ip}"
    username_key = f"login_limit:username:{username}"
    await redis_client.delete(ip_key)
    await redis_client.delete(username_key)
