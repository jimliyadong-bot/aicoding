"""
用户管理路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from passlib.context import CryptContext

from app.db.session import get_db
from app.models.user import AdminUser
from app.models.role import AdminRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse, ResetPasswordRequest, AssignRolesRequest
from app.schemas.response import success_response
from app.core.permissions import require_perm
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("", response_model=dict)
async def get_user_list(
    request: Request,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    username: Optional[str] = None,
    real_name: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:user:list"))
):
    """获取用户列表"""
    trace_id = getattr(request.state, "trace_id", "")
    
    # 构建查询
    stmt = select(AdminUser).where(AdminUser.deleted_at.is_(None))
    count_stmt = select(func.count(AdminUser.id)).where(AdminUser.deleted_at.is_(None))
    
    if username:
        stmt = stmt.where(AdminUser.username.like(f"%{username}%"))
        count_stmt = count_stmt.where(AdminUser.username.like(f"%{username}%"))
    if real_name:
        stmt = stmt.where(AdminUser.real_name.like(f"%{real_name}%"))
        count_stmt = count_stmt.where(AdminUser.real_name.like(f"%{real_name}%"))
    
    # 分页
    stmt = stmt.offset((page - 1) * size).limit(size).order_by(AdminUser.id.desc())
    
    # 执行查询
    result = await db.execute(stmt)
    users = result.scalars().all()
    
    count_result = await db.execute(count_stmt)
    total = count_result.scalar()
    
    return success_response(
        data={
            "items": [UserResponse.model_validate(u).model_dump() for u in users],
            "total": total,
            "page": page,
            "size": size
        },
        trace_id=trace_id
    )


@router.post("", response_model=dict)
async def create_user(
    request: Request,
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:user:create"))
):
    """创建用户"""
    trace_id = getattr(request.state, "trace_id", "")
    
    # 检查用户名是否存在
    stmt = select(AdminUser).where(AdminUser.username == user_data.username)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise BadRequestException("用户名已存在")
    
    # 创建用户
    user = AdminUser(
        username=user_data.username,
        password_hash=pwd_context.hash(user_data.password),
        real_name=user_data.real_name,
        phone=user_data.phone,
        email=user_data.email,
        status=user_data.status
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        message="创建成功",
        trace_id=trace_id
    )


@router.get("/{id}", response_model=dict)
async def get_user(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:user:detail"))
):
    """获取用户详情"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminUser).where(AdminUser.id == id, AdminUser.deleted_at.is_(None))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundException("用户不存在")
    
    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        trace_id=trace_id
    )


@router.put("/{id}", response_model=dict)
async def update_user(
    request: Request,
    id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:user:update"))
):
    """更新用户"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminUser).where(AdminUser.id == id, AdminUser.deleted_at.is_(None))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundException("用户不存在")
    
    # 更新字段
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    await db.commit()
    await db.refresh(user)
    
    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        message="更新成功",
        trace_id=trace_id
    )


@router.delete("/{id}", response_model=dict)
async def delete_user(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:user:delete"))
):
    """删除用户(软删除)"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminUser).where(AdminUser.id == id, AdminUser.deleted_at.is_(None))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundException("用户不存在")
    
    if user.id == current_user.id:
        raise BadRequestException("不能删除自己")
    
    # 软删除
    from datetime import datetime
    user.deleted_at = datetime.now()
    await db.commit()
    
    return success_response(message="删除成功", trace_id=trace_id)


@router.post("/{id}/reset-password", response_model=dict)
async def reset_password(
    request: Request,
    id: int,
    reset_data: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:user:reset"))
):
    """重置密码"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminUser).where(AdminUser.id == id, AdminUser.deleted_at.is_(None))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundException("用户不存在")
    
    user.password_hash = pwd_context.hash(reset_data.password)
    await db.commit()
    
    return success_response(message="密码重置成功", trace_id=trace_id)


@router.post("/{id}/roles", response_model=dict)
async def assign_roles(
    request: Request,
    id: int,
    assign_data: AssignRolesRequest,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(require_perm("sys:user:assign:role"))
):
    """分配角色"""
    trace_id = getattr(request.state, "trace_id", "")
    
    stmt = select(AdminUser).where(AdminUser.id == id, AdminUser.deleted_at.is_(None))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundException("用户不存在")
    
    # 获取角色
    role_stmt = select(AdminRole).where(AdminRole.id.in_(assign_data.role_ids))
    role_result = await db.execute(role_stmt)
    roles = role_result.scalars().all()
    
    # 分配角色
    user.roles = list(roles)
    await db.commit()
    
    return success_response(message="角色分配成功", trace_id=trace_id)
