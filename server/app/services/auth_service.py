"""
认证服务
"""
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.models.user import AdminUser
from app.schemas.auth import TokenResponse, RefreshTokenResponse
from app.utils.password import verify_password
from app.utils.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token_type
)
from app.core.config import settings
from app.core.exceptions import UnauthorizedException, BusinessException
from app.db.redis import redis_client


class AuthService:
    """认证服务"""
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        username: str,
        password: str
    ) -> Optional[AdminUser]:
        """
        验证用户
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            AdminUser: 用户对象,验证失败返回 None
        """
        # 查询用户
        stmt = select(AdminUser).where(
            AdminUser.username == username,
            AdminUser.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        # 验证密码
        if not verify_password(password, user.password_hash):
            return None
        
        # 检查用户状态
        if user.status != 1:
            raise BusinessException("用户已被禁用")
        
        return user
    
    @staticmethod
    async def login(
        db: AsyncSession,
        username: str,
        password: str,
        ip_address: str = ""
    ) -> TokenResponse:
        """
        用户登录
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            ip_address: IP 地址
            
        Returns:
            TokenResponse: Token 响应
            
        Raises:
            UnauthorizedException: 用户名或密码错误
        """
        # 验证用户
        user = await AuthService.authenticate_user(db, username, password)
        if not user:
            raise UnauthorizedException("用户名或密码错误")
        
        # 更新最后登录信息
        user.last_login_at = datetime.utcnow()
        user.last_login_ip = ip_address
        await db.commit()
        
        # 生成 Token
        token_data = {
            "sub": str(user.id),
            "username": user.username
        }
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        # 将 Refresh Token 存储到 Redis(用于黑名单检查)
        await redis_client.setex(
            f"refresh_token:{user.id}:{refresh_token}",
            settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # 转换为秒
            "1"
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    async def refresh_access_token(refresh_token: str) -> RefreshTokenResponse:
        """
        刷新 Access Token
        
        Args:
            refresh_token: Refresh Token
            
        Returns:
            RefreshTokenResponse: 新的 Access Token
            
        Raises:
            UnauthorizedException: Token 无效或已过期
        """
        try:
            # 解码 Token
            payload = decode_token(refresh_token)
            
            # 验证 Token 类型
            if not verify_token_type(payload, "refresh"):
                raise UnauthorizedException("Token 类型错误")
            
            # 检查 Token 是否在黑名单中
            user_id = payload.get("sub")
            is_blacklisted = await redis_client.get(f"token:blacklist:{refresh_token}")
            if is_blacklisted:
                raise UnauthorizedException("Token 已失效")
            
            # 检查 Token 是否存在于 Redis
            token_exists = await redis_client.get(f"refresh_token:{user_id}:{refresh_token}")
            if not token_exists:
                raise UnauthorizedException("Token 不存在或已过期")
            
            # 生成新的 Access Token
            token_data = {
                "sub": user_id,
                "username": payload.get("username")
            }
            access_token = create_access_token(token_data)
            
            return RefreshTokenResponse(
                access_token=access_token,
                token_type="Bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
            
        except JWTError:
            raise UnauthorizedException("Token 无效或已过期")
    
    @staticmethod
    async def logout(user_id: int, refresh_token: str) -> None:
        """
        用户登出
        
        Args:
            user_id: 用户 ID
            refresh_token: Refresh Token
        """
        try:
            # 解码 Token 获取过期时间
            payload = decode_token(refresh_token)
            exp = payload.get("exp")
            
            if exp:
                # 计算剩余有效期
                now = datetime.utcnow().timestamp()
                ttl = int(exp - now)
                
                if ttl > 0:
                    # 将 Token 加入黑名单
                    await redis_client.setex(
                        f"token:blacklist:{refresh_token}",
                        ttl,
                        "1"
                    )
            
            # 删除 Redis 中的 Refresh Token
            await redis_client.delete(f"refresh_token:{user_id}:{refresh_token}")
            
        except JWTError:
            # Token 无效时也认为登出成功
            pass
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[AdminUser]:
        """
        根据 ID 获取用户
        
        Args:
            db: 数据库会话
            user_id: 用户 ID
            
        Returns:
            AdminUser: 用户对象(包含角色和菜单关系)
        """
        from sqlalchemy.orm import selectinload
        from app.models.role import AdminRole
        
        stmt = select(AdminUser).options(
            selectinload(AdminUser.roles).selectinload(AdminRole.menus),
            selectinload(AdminUser.roles).selectinload(AdminRole.permissions)
        ).where(
            AdminUser.id == user_id,
            AdminUser.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
