"""
依赖注入
"""
from typing import Optional, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import decode_token


# HTTP Bearer 认证
security = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    获取当前用户ID
    
    Args:
        credentials: HTTP认证凭证
        
    Returns:
        int: 用户ID
        
    Raises:
        HTTPException: Token无效或过期
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效或已过期",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token无效",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return int(user_id)


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户对象
    
    Args:
        user_id: 用户ID
        db: 数据库会话
        
    Returns:
        User: 用户对象
        
    Raises:
        HTTPException: 用户不存在
    """
    # TODO: 从数据库查询用户
    # from app.models.user import User
    # user = await db.get(User, user_id)
    # if user is None or user.deleted_at is not None:
    #     raise HTTPException(status_code=404, detail="用户不存在")
    # return user
    pass
