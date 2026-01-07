"""
菜单管理路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import AdminUser
from app.schemas.menu import MenuCreate, MenuUpdate, MenuTreeNode, MenuRoute, MenuSortUpdate
from app.schemas.response import success_response
from app.services.menu_service import MenuService
from app.core.dependencies import get_current_user
from app.core.permissions import require_perm

router = APIRouter()


@router.get("/tree", response_model=dict)
async def get_menu_tree(
    request: Request,
    include_disabled: bool = False,
    current_user: AdminUser = Depends(require_perm("sys:menu:list")),
    db: AsyncSession = Depends(get_db)
):
    """
    获取菜单树
    
    Args:
        request: 请求对象
        include_disabled: 是否包含禁用的菜单
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 菜单树
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    tree = await MenuService.get_menu_tree(db, include_disabled)
    
    return success_response(
        data=[node.model_dump() for node in tree],
        message="获取菜单树成功",
        trace_id=trace_id
    )


@router.get("/my", response_model=dict)
async def get_my_menu_tree(
    request: Request,
    current_user: AdminUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取我的菜单树(用于前端动态路由)
    
    Args:
        request: 请求对象
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 菜单路由树
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    routes = await MenuService.get_my_menu_tree(db, current_user)
    
    return success_response(
        data=[route.model_dump() for route in routes],
        message="获取我的菜单树成功",
        trace_id=trace_id
    )


@router.post("", response_model=dict)
async def create_menu(
    request: Request,
    menu_data: MenuCreate,
    current_user: AdminUser = Depends(require_perm("sys:menu:create")),
    db: AsyncSession = Depends(get_db)
):
    """
    创建菜单
    
    Args:
        request: 请求对象
        menu_data: 菜单数据
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 创建的菜单
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    menu = await MenuService.create_menu(db, menu_data.model_dump())
    
    return success_response(
        data={
            "id": menu.id,
            "name": menu.name,
            "title": menu.title
        },
        message="创建菜单成功",
        trace_id=trace_id
    )


@router.put("/{menu_id}", response_model=dict)
async def update_menu(
    request: Request,
    menu_id: int,
    menu_data: MenuUpdate,
    current_user: AdminUser = Depends(require_perm("sys:menu:update")),
    db: AsyncSession = Depends(get_db)
):
    """
    更新菜单
    
    Args:
        request: 请求对象
        menu_id: 菜单 ID
        menu_data: 菜单数据
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 更新后的菜单
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 过滤掉 None 值
    update_data = {k: v for k, v in menu_data.model_dump().items() if v is not None}
    
    menu = await MenuService.update_menu(db, menu_id, update_data)
    
    return success_response(
        data={
            "id": menu.id,
            "name": menu.name,
            "title": menu.title
        },
        message="更新菜单成功",
        trace_id=trace_id
    )


@router.delete("/{menu_id}", response_model=dict)
async def delete_menu(
    request: Request,
    menu_id: int,
    current_user: AdminUser = Depends(require_perm("sys:menu:delete")),
    db: AsyncSession = Depends(get_db)
):
    """
    删除菜单(级联删除子菜单)
    
    Args:
        request: 请求对象
        menu_id: 菜单 ID
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 删除结果
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    await MenuService.delete_menu(db, menu_id)
    
    return success_response(
        data=None,
        message="删除菜单成功",
        trace_id=trace_id
    )


@router.put("/{menu_id}/sort", response_model=dict)
async def update_menu_sort(
    request: Request,
    menu_id: int,
    sort_data: MenuSortUpdate,
    current_user: AdminUser = Depends(require_perm("sys:menu:update")),
    db: AsyncSession = Depends(get_db)
):
    """
    更新菜单排序
    
    Args:
        request: 请求对象
        menu_id: 菜单 ID
        sort_data: 排序数据
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 更新结果
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    menu = await MenuService.update_menu(db, menu_id, {"sort": sort_data.sort})
    
    return success_response(
        data={
            "id": menu.id,
            "sort": menu.sort
        },
        message="更新排序成功",
        trace_id=trace_id
    )
