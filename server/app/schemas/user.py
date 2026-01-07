"""
用户管理相关 Schema
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """用户基础 Schema"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    email: Optional[str] = Field(None, max_length=100, description="邮箱")
    status: int = Field(default=1, description="状态: 0-禁用, 1-启用")


class UserCreate(UserBase):
    """创建用户 Schema"""
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class UserUpdate(BaseModel):
    """更新用户 Schema"""
    real_name: Optional[str] = Field(None, max_length=50, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    email: Optional[str] = Field(None, max_length=100, description="邮箱")
    status: Optional[int] = Field(None, description="状态: 0-禁用, 1-启用")


class UserResponse(BaseModel):
    """用户响应 Schema"""
    id: int
    username: str
    real_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ResetPasswordRequest(BaseModel):
    """重置密码请求"""
    password: str = Field(..., min_length=6, max_length=100, description="新密码")


class AssignRolesRequest(BaseModel):
    """分配角色请求"""
    role_ids: List[int] = Field(..., description="角色ID列表")
