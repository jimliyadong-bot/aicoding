"""
菜单相关 Schema
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    """菜单基础 Schema"""
    parent_id: int = Field(default=0, description="父菜单ID(0为根节点)")
    title: str = Field(..., description="菜单标题", min_length=1, max_length=50)
    name: str = Field(..., description="路由名称(唯一)", min_length=1, max_length=50)
    path: Optional[str] = Field(None, description="路由路径", max_length=200)
    component: Optional[str] = Field(None, description="组件路径", max_length=200)
    icon: Optional[str] = Field(None, description="菜单图标", max_length=50)
    sort: int = Field(default=0, description="排序号(升序)")
    hidden: int = Field(default=0, description="是否隐藏: 0-显示, 1-隐藏")
    keep_alive: int = Field(default=1, description="是否缓存: 0-不缓存, 1-缓存")
    status: int = Field(default=1, description="状态: 0-禁用, 1-启用")


class MenuCreate(MenuBase):
    """创建菜单 Schema"""
    pass


class MenuUpdate(BaseModel):
    """更新菜单 Schema"""
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    title: Optional[str] = Field(None, description="菜单标题", min_length=1, max_length=50)
    name: Optional[str] = Field(None, description="路由名称", min_length=1, max_length=50)
    path: Optional[str] = Field(None, description="路由路径", max_length=200)
    component: Optional[str] = Field(None, description="组件路径", max_length=200)
    icon: Optional[str] = Field(None, description="菜单图标", max_length=50)
    sort: Optional[int] = Field(None, description="排序号")
    hidden: Optional[int] = Field(None, description="是否隐藏")
    keep_alive: Optional[int] = Field(None, description="是否缓存")
    status: Optional[int] = Field(None, description="状态")


class MenuTreeNode(BaseModel):
    """菜单树节点 Schema"""
    id: int = Field(..., description="菜单ID")
    parent_id: int = Field(..., description="父菜单ID")
    title: str = Field(..., description="菜单标题")
    name: str = Field(..., description="路由名称")
    path: Optional[str] = Field(None, description="路由路径")
    component: Optional[str] = Field(None, description="组件路径")
    icon: Optional[str] = Field(None, description="菜单图标")
    sort: int = Field(..., description="排序号")
    hidden: int = Field(..., description="是否隐藏")
    keep_alive: int = Field(..., description="是否缓存")
    status: int = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")
    children: List["MenuTreeNode"] = Field(default_factory=list, description="子菜单")
    
    class Config:
        from_attributes = True


class MenuMeta(BaseModel):
    """菜单元数据(前端使用)"""
    icon: Optional[str] = Field(None, description="图标")
    title: str = Field(..., description="标题")
    hidden: bool = Field(default=False, description="是否隐藏")
    keepAlive: bool = Field(default=True, description="是否缓存")


class MenuRoute(BaseModel):
    """菜单路由 Schema(前端动态路由使用)"""
    id: int = Field(..., description="菜单ID")
    title: str = Field(..., description="菜单标题")
    name: str = Field(..., description="路由名称")
    path: str = Field(..., description="路由路径")
    component: str = Field(..., description="组件路径")
    meta: MenuMeta = Field(..., description="元数据")
    children: List["MenuRoute"] = Field(default_factory=list, description="子路由")


class MenuSortUpdate(BaseModel):
    """更新菜单排序 Schema"""
    sort: int = Field(..., description="排序号", ge=0)
