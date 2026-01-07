"""
权限管理相关 Schema
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    """权限基础 Schema"""
    name: str = Field(..., min_length=2, max_length=50, description="权限名称")
    code: str = Field(..., min_length=2, max_length=100, description="权限编码")
    type: str = Field(default="API", description="类型: MENU/BUTTON/API")
    description: Optional[str] = Field(None, max_length=200, description="描述")


class PermissionCreate(PermissionBase):
    """创建权限 Schema"""
    pass


class PermissionUpdate(BaseModel):
    """更新权限 Schema"""
    name: Optional[str] = Field(None, max_length=50, description="权限名称")
    type: Optional[str] = Field(None, description="类型: MENU/BUTTON/API")
    description: Optional[str] = Field(None, max_length=200, description="描述")


class PermissionResponse(BaseModel):
    """权限响应 Schema"""
    id: int
    name: str
    code: str
    type: str
    description: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
