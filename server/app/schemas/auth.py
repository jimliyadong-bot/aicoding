"""
认证相关 Schema
"""
from datetime import datetime
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., description="用户名", min_length=3, max_length=50)
    password: str = Field(..., description="密码", min_length=6, max_length=50)


class TokenResponse(BaseModel):
    """Token 响应"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="Bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")


class RefreshTokenRequest(BaseModel):
    """刷新 Token 请求"""
    refresh_token: str = Field(..., description="刷新令牌")


class RefreshTokenResponse(BaseModel):
    """刷新 Token 响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="Bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")


class LogoutRequest(BaseModel):
    """登出请求"""
    refresh_token: str = Field(..., description="刷新令牌")


class UserInfoResponse(BaseModel):
    """用户信息响应"""
    id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    real_name: str | None = Field(None, description="真实姓名")
    email: str | None = Field(None, description="邮箱")
    phone: str | None = Field(None, description="手机号")
    avatar: str | None = Field(None, description="头像URL")
    status: int = Field(..., description="状态: 0-禁用, 1-启用")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True
