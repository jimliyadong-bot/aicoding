"""
角色管理相关 Schema
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """角色基础 Schema"""
    name: str = Field(..., min_length=2, max_length=50, description="角色名称")
    code: str = Field(..., min_length=2, max_length=50, description="角色编码")
    description: Optional[str] = Field(None, max_length=200, description="描述")
    status: int = Field(default=1, description="状态: 0-禁用, 1-启用")


class RoleCreate(RoleBase):
    """创建角色 Schema"""
    pass


class RoleUpdate(BaseModel):
    """更新角色 Schema"""
    name: Optional[str] = Field(None, max_length=50, description="角色名称")
    description: Optional[str] = Field(None, max_length=200, description="描述")
    status: Optional[int] = Field(None, description="状态: 0-禁用, 1-启用")


class RoleResponse(BaseModel):
    """角色响应 Schema"""
    id: int
    name: str
    code: str
    description: Optional[str] = None
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AssignPermissionsRequest(BaseModel):
    """分配权限请求"""
    permission_ids: List[int] = Field(..., description="权限ID列表")


class AssignMenusRequest(BaseModel):
    """分配菜单请求"""
    menu_ids: List[int] = Field(..., description="菜单ID列表")
