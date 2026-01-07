"""
权限管理路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import AdminUser
from app.models.permission import AdminPermission
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionResponse
from app.schemas.response import success_response
from app.core.dependencies import get_current_user
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()


@router.get("", response_model=dict)
async def get_permission_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """获取权限列表"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminPermission).where(AdminPermission.deleted_at.is_(None)).order_by(AdminPermission.id)
    result = await db.execute(stmt)
    permissions = result.scalars().all()
    
    return success_response(
        data=[PermissionResponse.model_validate(p).model_dump() for p in permissions],
        trace_id=trace_id
    )


@router.get("/tree", response_model=dict)
async def get_permission_tree(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """获取权限树(用于角色绑定)"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminPermission).where(AdminPermission.deleted_at.is_(None)).order_by(AdminPermission.id)
    result = await db.execute(stmt)
    permissions = result.scalars().all()
    
    # 简单返回列表,前端可以按需构建树
    return success_response(
        data=[{"id": p.id, "name": p.name, "code": p.code, "type": p.type} for p in permissions],
        trace_id=trace_id
    )


@router.post("", response_model=dict)
async def create_permission(
    request: Request,
    perm_data: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """创建权限"""
    trace_id = getattr(request.state, "trace_id", "")
    
    # 检查编码是否存在
    stmt = select(AdminPermission).where(AdminPermission.code == perm_data.code)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise BadRequestException("权限编码已存在")
    
    permission = AdminPermission(
        name=perm_data.name,
        code=perm_data.code,
        type=perm_data.type,
        description=perm_data.description
    )
    db.add(permission)
    await db.commit()
    await db.refresh(permission)
    
    return success_response(
        data=PermissionResponse.model_validate(permission).model_dump(),
        message="创建成功",
        trace_id=trace_id
    )


@router.get("/{id}", response_model=dict)
async def get_permission(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """获取权限详情"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminPermission).where(AdminPermission.id == id, AdminPermission.deleted_at.is_(None))
    result = await db.execute(stmt)
    permission = result.scalar_one_or_none()
    
    if not permission:
        raise NotFoundException("权限不存在")
    
    return success_response(
        data=PermissionResponse.model_validate(permission).model_dump(),
        trace_id=trace_id
    )


@router.put("/{id}", response_model=dict)
async def update_permission(
    request: Request,
    id: int,
    perm_data: PermissionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """更新权限"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminPermission).where(AdminPermission.id == id, AdminPermission.deleted_at.is_(None))
    result = await db.execute(stmt)
    permission = result.scalar_one_or_none()
    
    if not permission:
        raise NotFoundException("权限不存在")
    
    update_data = perm_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(permission, key, value)
    
    await db.commit()
    await db.refresh(permission)
    
    return success_response(
        data=PermissionResponse.model_validate(permission).model_dump(),
        message="更新成功",
        trace_id=trace_id
    )


@router.delete("/{id}", response_model=dict)
async def delete_permission(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """删除权限"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminPermission).where(AdminPermission.id == id, AdminPermission.deleted_at.is_(None))
    result = await db.execute(stmt)
    permission = result.scalar_one_or_none()
    
    if not permission:
        raise NotFoundException("权限不存在")
    
    from datetime import datetime
    permission.deleted_at = datetime.now()
    await db.commit()
    
    return success_response(message="删除成功", trace_id=trace_id)
