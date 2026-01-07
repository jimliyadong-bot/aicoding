"""
小程序用户相关 Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class LoginByCodeRequest(BaseModel):
    """通过 code 登录请求"""
    code: str = Field(..., description="wx.login 返回的 code")


class LoginResponse(BaseModel):
    """登录响应"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="Bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")
    is_new_user: bool = Field(..., description="是否新用户")
    need_bind_phone: bool = Field(..., description="是否需要绑定手机号")


class BindPhoneRequest(BaseModel):
    """绑定手机号请求"""
    code: str = Field(..., description="getPhoneNumber 返回的 code")


class BindPhoneResponse(BaseModel):
    """绑定手机号响应"""
    phone: str = Field(..., description="手机号")


class MiniProgramUserInfo(BaseModel):
    """小程序用户信息"""
    id: int = Field(..., description="用户ID")
    openid: str = Field(..., description="微信 openid")
    nickname: Optional[str] = Field(None, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")
    phone: Optional[str] = Field(None, description="手机号")
    gender: Optional[int] = Field(None, description="性别")
    country: Optional[str] = Field(None, description="国家")
    province: Optional[str] = Field(None, description="省份")
    city: Optional[str] = Field(None, description="城市")
    created_at: datetime = Field(..., description="创建时间")
    
    class Config:
        from_attributes = True


class UpdateUserInfoRequest(BaseModel):
    """更新用户信息请求"""
    nickname: Optional[str] = Field(None, description="昵称", max_length=100)
    avatar: Optional[str] = Field(None, description="头像URL", max_length=500)
