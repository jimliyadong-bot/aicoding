"""
角色管理路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.user import AdminUser
from app.models.role import AdminRole
from app.models.permission import AdminPermission
from app.models.menu import AdminMenu
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse, AssignPermissionsRequest, AssignMenusRequest
from app.schemas.response import success_response
from app.core.permissions import require_perm
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()


@router.get("", response_model=dict)
async def get_role_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:role:list"))
):
    """获取角色列表"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminRole).where(AdminRole.deleted_at.is_(None)).order_by(AdminRole.id)
    result = await db.execute(stmt)
    roles = result.scalars().all()
    
    return success_response(
        data=[RoleResponse.model_validate(r).model_dump() for r in roles],
        trace_id=trace_id
    )


@router.post("", response_model=dict)
async def create_role(
    request: Request,
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:role:create"))
):
    """创建角色"""
    trace_id = getattr(request.state, "trace_id", "")
    
    # 检查编码是否存在
    stmt = select(AdminRole).where(AdminRole.code == role_data.code)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise BadRequestException("角色编码已存在")
    
    role = AdminRole(
        name=role_data.name,
        code=role_data.code,
        description=role_data.description,
        status=role_data.status
    )
    db.add(role)
    await db.commit()
    await db.refresh(role)
    
    return success_response(
        data=RoleResponse.model_validate(role).model_dump(),
        message="创建成功",
        trace_id=trace_id
    )


@router.get("/{id}", response_model=dict)
async def get_role(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:role:detail"))
):
    """获取角色详情"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminRole).where(AdminRole.id == id, AdminRole.deleted_at.is_(None))
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    
    if not role:
        raise NotFoundException("角色不存在")
    
    return success_response(
        data=RoleResponse.model_validate(role).model_dump(),
        trace_id=trace_id
    )


@router.put("/{id}", response_model=dict)
async def update_role(
    request: Request,
    id: int,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:role:update"))
):
    """更新角色"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminRole).where(AdminRole.id == id, AdminRole.deleted_at.is_(None))
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    
    if not role:
        raise NotFoundException("角色不存在")
    
    update_data = role_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(role, key, value)
    
    await db.commit()
    await db.refresh(role)
    
    return success_response(
        data=RoleResponse.model_validate(role).model_dump(),
        message="更新成功",
        trace_id=trace_id
    )


@router.delete("/{id}", response_model=dict)
async def delete_role(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:role:delete"))
):
    """删除角色"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminRole).where(AdminRole.id == id, AdminRole.deleted_at.is_(None))
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    
    if not role:
        raise NotFoundException("角色不存在")
    
    if role.code == "SUPER_ADMIN":
        raise BadRequestException("不能删除超级管理员角色")
    
    from datetime import datetime
    role.deleted_at = datetime.now()
    await db.commit()
    
    return success_response(message="删除成功", trace_id=trace_id)


@router.get("/{id}/permissions", response_model=dict)
async def get_role_permissions(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:role:assign:permission"))
):
    """获取角色权限"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminRole).options(selectinload(AdminRole.permissions)).where(AdminRole.id == id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    
    if not role:
        raise NotFoundException("角色不存在")
    
    return success_response(
        data=[{"id": p.id, "name": p.name, "code": p.code} for p in role.permissions],
        trace_id=trace_id
    )


@router.post("/{id}/permissions", response_model=dict)
async def assign_permissions(
    request: Request,
    id: int,
    assign_data: AssignPermissionsRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:role:assign:permission"))
):
    """绑定权限"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminRole).options(selectinload(AdminRole.permissions)).where(AdminRole.id == id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    
    if not role:
        raise NotFoundException("角色不存在")
    
    perm_stmt = select(AdminPermission).where(AdminPermission.id.in_(assign_data.permission_ids))
    perm_result = await db.execute(perm_stmt)
    permissions = perm_result.scalars().all()
    
    role.permissions = list(permissions)
    await db.commit()
    
    return success_response(message="权限绑定成功", trace_id=trace_id)


@router.get("/{id}/menus", response_model=dict)
async def get_role_menus(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:role:assign:menu"))
):
    """获取角色菜单"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminRole).options(selectinload(AdminRole.menus)).where(AdminRole.id == id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    
    if not role:
        raise NotFoundException("角色不存在")
    
    return success_response(
        data=[{"id": m.id, "title": m.title, "name": m.name} for m in role.menus],
        trace_id=trace_id
    )


@router.post("/{id}/menus", response_model=dict)
async def assign_menus(
    request: Request,
    id: int,
    assign_data: AssignMenusRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:role:assign:menu"))
):
    """绑定菜单"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminRole).options(selectinload(AdminRole.menus)).where(AdminRole.id == id)
    result = await db.execute(stmt)
    role = result.scalar_one_or_none()
    
    if not role:
        raise NotFoundException("角色不存在")
    
    menu_stmt = select(AdminMenu).where(AdminMenu.id.in_(assign_data.menu_ids))
    menu_result = await db.execute(menu_stmt)
    menus = menu_result.scalars().all()
    
    role.menus = list(menus)
    await db.commit()
    
    return success_response(message="菜单绑定成功", trace_id=trace_id)
