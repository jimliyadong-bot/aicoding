"""
权限服务
"""
from typing import List, Set
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import AdminUser
from app.models.role import AdminRole
from app.models.permission import AdminPermission


class PermissionService:
    """权限服务"""
    
    @staticmethod
    def is_super_admin(user: AdminUser) -> bool:
        """
        判断是否为超级管理员
        
        Args:
            user: 用户对象
            
        Returns:
            bool: 是否为超级管理员
        """
        if not user.roles:
            return False
        
        for role in user.roles:
            if role.code == "SUPER_ADMIN":
                return True
        
        return False
    
    @staticmethod
    def get_user_permissions(user: AdminUser) -> Set[str]:
        """
        获取用户的所有权限编码
        
        Args:
            user: 用户对象
            
        Returns:
            Set[str]: 权限编码集合
        """
        permissions = set()
        
        if not user.roles:
            return permissions
        
        for role in user.roles:
            if role.permissions:
                for permission in role.permissions:
                    permissions.add(permission.code)
        
        return permissions
    
    @staticmethod
    def has_permission(user: AdminUser, permission_code: str) -> bool:
        """
        检查用户是否有指定权限
        
        Args:
            user: 用户对象
            permission_code: 权限编码
            
        Returns:
            bool: 是否有权限
        """
        # 超级管理员拥有所有权限
        if PermissionService.is_super_admin(user):
            return True
        
        # 获取用户权限
        user_permissions = PermissionService.get_user_permissions(user)
        
        # 检查是否有指定权限
        return permission_code in user_permissions
    
    @staticmethod
    def has_any_permission(user: AdminUser, permission_codes: List[str]) -> bool:
        """
        检查用户是否有任意一个权限
        
        Args:
            user: 用户对象
            permission_codes: 权限编码列表
            
        Returns:
            bool: 是否有任意权限
        """
        # 超级管理员拥有所有权限
        if PermissionService.is_super_admin(user):
            return True
        
        # 获取用户权限
        user_permissions = PermissionService.get_user_permissions(user)
        
        # 检查是否有任意权限
        for code in permission_codes:
            if code in user_permissions:
                return True
        
        return False
    
    @staticmethod
    def has_all_permissions(user: AdminUser, permission_codes: List[str]) -> bool:
        """
        检查用户是否有所有权限
        
        Args:
            user: 用户对象
            permission_codes: 权限编码列表
            
        Returns:
            bool: 是否有所有权限
        """
        # 超级管理员拥有所有权限
        if PermissionService.is_super_admin(user):
            return True
        
        # 获取用户权限
        user_permissions = PermissionService.get_user_permissions(user)
        
        # 检查是否有所有权限
        for code in permission_codes:
            if code not in user_permissions:
                return False
        
        return True
