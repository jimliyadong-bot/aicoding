"""
认证依赖
"""
from typing import Optional
from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import JWTError

from app.db.session import get_db
from app.models.user import AdminUser
from app.models.mp_user import MiniProgramUser
from app.services.auth_service import AuthService
from app.utils.jwt import decode_token, verify_token_type
from app.core.exceptions import UnauthorizedException

# HTTP Bearer 认证
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> AdminUser:
    """
    获取当前登录用户
    
    Args:
        credentials: HTTP 认证凭证
        db: 数据库会话
        
    Returns:
        AdminUser: 当前用户
        
    Raises:
        UnauthorizedException: Token 无效或用户不存在
    """
    token = credentials.credentials
    
    try:
        # 解码 Token
        payload = decode_token(token)
        
        # 验证 Token 类型
        if not verify_token_type(payload, "access"):
            raise UnauthorizedException("Token 类型错误")
        
        # 获取用户 ID
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException("Token 无效")
        
        # 查询用户
        user = await AuthService.get_user_by_id(db, int(user_id))
        if user is None:
            raise UnauthorizedException("用户不存在")
        
        # 检查用户状态
        if user.status != 1:
            raise UnauthorizedException("用户已被禁用")
        
        return user
        
    except JWTError:
        raise UnauthorizedException("Token 无效或已过期")


async def get_current_active_user(
    current_user: AdminUser = Depends(get_current_user)
) -> AdminUser:
    """
    获取当前活跃用户(状态为启用)
    
    Args:
        current_user: 当前用户
        
    Returns:
        AdminUser: 当前活跃用户
        
    Raises:
        UnauthorizedException: 用户已被禁用
    """
    if current_user.status != 1:
        raise UnauthorizedException("用户已被禁用")
    return current_user


async def get_current_mp_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> MiniProgramUser:
    """
    获取当前小程序用户
    
    Args:
        credentials: HTTP 认证凭证
        db: 数据库会话
        
    Returns:
        MiniProgramUser: 当前小程序用户
        
    Raises:
        UnauthorizedException: Token 无效或用户不存在
    """
    token = credentials.credentials
    
    try:
        # 解码 Token
        payload = decode_token(token)
        
        # 验证 Token 类型
        if not verify_token_type(payload, "access"):
            raise UnauthorizedException("Token 类型错误")
        
        # 获取用户 ID
        user_id: str = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException("Token 无效")
        
        # 查询小程序用户
        stmt = select(MiniProgramUser).where(MiniProgramUser.id == int(user_id))
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user is None:
            raise UnauthorizedException("用户不存在")
        
        return user
        
    except JWTError:
        raise UnauthorizedException("Token 无效或已过期")
