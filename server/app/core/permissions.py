"""
权限依赖和装饰器
"""
from typing import List
from fastapi import Depends
from app.core.dependencies import get_current_user
from app.models.user import AdminUser
from app.services.permission_service import PermissionService
from app.core.exceptions import ForbiddenException


def require_perm(permission_code: str):
    """
    权限验证依赖(单个权限)
    
    Args:
        permission_code: 权限编码(如: sys:user:list)
        
    Returns:
        依赖函数
        
    Example:
        @router.get("/users")
        async def get_users(
            current_user: AdminUser = Depends(require_perm("sys:user:list"))
        ):
            return {"users": []}
    """
    async def permission_checker(
        current_user: AdminUser = Depends(get_current_user)
    ) -> AdminUser:
        """检查权限"""
        # 检查是否有指定权限
        if not PermissionService.has_permission(current_user, permission_code):
            raise ForbiddenException(f"缺少权限: {permission_code}")
        
        return current_user
    
    return permission_checker


def require_any_perm(*permission_codes: str):
    """
    权限验证依赖(任意权限)
    
    Args:
        permission_codes: 权限编码列表
        
    Returns:
        依赖函数
        
    Example:
        @router.get("/users")
        async def get_users(
            current_user: AdminUser = Depends(require_any_perm("sys:user:list", "sys:user:view"))
        ):
            return {"users": []}
    """
    async def permission_checker(
        current_user: AdminUser = Depends(get_current_user)
    ) -> AdminUser:
        """检查权限"""
        # 检查是否有任意权限
        if not PermissionService.has_any_permission(current_user, list(permission_codes)):
            raise ForbiddenException(f"缺少权限: {' 或 '.join(permission_codes)}")
        
        return current_user
    
    return permission_checker


def require_all_perms(*permission_codes: str):
    """
    权限验证依赖(所有权限)
    
    Args:
        permission_codes: 权限编码列表
        
    Returns:
        依赖函数
        
    Example:
        @router.post("/users")
        async def create_user(
            current_user: AdminUser = Depends(require_all_perms("sys:user:create", "sys:user:assign"))
        ):
            return {"message": "创建成功"}
    """
    async def permission_checker(
        current_user: AdminUser = Depends(get_current_user)
    ) -> AdminUser:
        """检查权限"""
        # 检查是否有所有权限
        if not PermissionService.has_all_permissions(current_user, list(permission_codes)):
            raise ForbiddenException(f"缺少权限: {' 和 '.join(permission_codes)}")
        
        return current_user
    
    return permission_checker


def require_super_admin():
    """
    超级管理员验证依赖
    
    Returns:
        依赖函数
        
    Example:
        @router.delete("/system/reset")
        async def reset_system(
            current_user: AdminUser = Depends(require_super_admin())
        ):
            return {"message": "系统重置成功"}
    """
    async def super_admin_checker(
        current_user: AdminUser = Depends(get_current_user)
    ) -> AdminUser:
        """检查是否为超级管理员"""
        if not PermissionService.is_super_admin(current_user):
            raise ForbiddenException("需要超级管理员权限")
        
        return current_user
    
    return super_admin_checker
