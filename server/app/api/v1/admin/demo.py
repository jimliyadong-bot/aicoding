"""
示例接口 - 演示权限验证
"""
from fastapi import APIRouter, Depends, Request
from app.models.user import AdminUser
from app.core.permissions import require_perm, require_any_perm, require_super_admin
from app.schemas.response import success_response
from app.services.permission_service import PermissionService

router = APIRouter()


@router.get("/need_perm")
async def demo_need_perm(
    request: Request,
    current_user: AdminUser = Depends(require_perm("sys:demo:view"))
):
    """
    需要 sys:demo:view 权限的示例接口
    
    Args:
        request: 请求对象
        current_user: 当前用户
        
    Returns:
        dict: 响应数据
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 获取用户权限列表
    permissions = PermissionService.get_user_permissions(current_user)
    
    return success_response(
        data={
            "message": "你有权限访问此接口",
            "user": current_user.username,
            "required_permission": "sys:demo:view",
            "user_permissions": list(permissions),
            "is_super_admin": PermissionService.is_super_admin(current_user)
        },
        trace_id=trace_id
    )


@router.get("/need_any_perm")
async def demo_need_any_perm(
    request: Request,
    current_user: AdminUser = Depends(require_any_perm("sys:demo:view", "sys:demo:list"))
):
    """
    需要 sys:demo:view 或 sys:demo:list 任意权限的示例接口
    
    Args:
        request: 请求对象
        current_user: 当前用户
        
    Returns:
        dict: 响应数据
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    return success_response(
        data={
            "message": "你有权限访问此接口(任意权限)",
            "user": current_user.username,
            "required_permissions": ["sys:demo:view", "sys:demo:list"],
            "match_type": "any"
        },
        trace_id=trace_id
    )


@router.get("/super_admin_only")
async def demo_super_admin_only(
    request: Request,
    current_user: AdminUser = Depends(require_super_admin())
):
    """
    仅超级管理员可访问的示例接口
    
    Args:
        request: 请求对象
        current_user: 当前用户
        
    Returns:
        dict: 响应数据
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    return success_response(
        data={
            "message": "欢迎,超级管理员!",
            "user": current_user.username,
            "roles": [role.code for role in current_user.roles]
        },
        trace_id=trace_id
    )


@router.get("/public")
async def demo_public(request: Request):
    """
    公开接口(无需权限)
    
    Args:
        request: 请求对象
        
    Returns:
        dict: 响应数据
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    return success_response(
        data={
            "message": "这是公开接口,无需权限即可访问"
        },
        trace_id=trace_id
    )
