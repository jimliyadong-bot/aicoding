"""
菜单服务
"""
from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.menu import AdminMenu
from app.models.user import AdminUser
from app.schemas.menu import MenuTreeNode, MenuRoute, MenuMeta
from app.services.permission_service import PermissionService
from app.core.exceptions import NotFoundException, BusinessException


class MenuService:
    """菜单服务"""
    
    @staticmethod
    async def get_menu_tree(db: AsyncSession, include_disabled: bool = False) -> List[MenuTreeNode]:
        """
        获取菜单树
        
        Args:
            db: 数据库会话
            include_disabled: 是否包含禁用的菜单
            
        Returns:
            List[MenuTreeNode]: 菜单树
        """
        # 查询所有菜单
        stmt = select(AdminMenu).where(AdminMenu.deleted_at.is_(None))
        if not include_disabled:
            stmt = stmt.where(AdminMenu.status == 1)
        stmt = stmt.order_by(AdminMenu.sort.asc(), AdminMenu.id.asc())
        
        result = await db.execute(stmt)
        menus = result.scalars().all()
        
        # 构建树形结构
        return MenuService._build_tree(menus, 0)
    
    @staticmethod
    async def get_my_menu_tree(db: AsyncSession, user: AdminUser) -> List[MenuRoute]:
        """
        获取当前用户的菜单树(用于前端动态路由)
        
        Args:
            db: 数据库会话
            user: 当前用户
            
        Returns:
            List[MenuRoute]: 菜单路由树
        """
        # 超级管理员返回所有菜单
        if PermissionService.is_super_admin(user):
            stmt = select(AdminMenu).where(
                AdminMenu.deleted_at.is_(None),
                AdminMenu.status == 1
            ).order_by(AdminMenu.sort.asc(), AdminMenu.id.asc())
            result = await db.execute(stmt)
            menus = result.scalars().all()
        else:
            # 普通用户根据角色获取菜单
            menu_ids = set()
            for role in user.roles:
                if role.menus:
                    for menu in role.menus:
                        if menu.status == 1 and menu.deleted_at is None:
                            menu_ids.add(menu.id)
            
            if not menu_ids:
                return []
            
            stmt = select(AdminMenu).where(
                AdminMenu.id.in_(menu_ids),
                AdminMenu.deleted_at.is_(None),
                AdminMenu.status == 1
            ).order_by(AdminMenu.sort.asc(), AdminMenu.id.asc())
            result = await db.execute(stmt)
            menus = result.scalars().all()
        
        # 构建树形结构
        tree = MenuService._build_tree(menus, 0)
        
        # 转换为前端路由格式
        return MenuService._convert_to_routes(tree)
    
    @staticmethod
    async def get_menu_by_id(db: AsyncSession, menu_id: int) -> Optional[AdminMenu]:
        """
        根据 ID 获取菜单
        
        Args:
            db: 数据库会话
            menu_id: 菜单 ID
            
        Returns:
            AdminMenu: 菜单对象
        """
        stmt = select(AdminMenu).where(
            AdminMenu.id == menu_id,
            AdminMenu.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_menu(db: AsyncSession, menu_data: dict) -> AdminMenu:
        """
        创建菜单
        
        Args:
            db: 数据库会话
            menu_data: 菜单数据
            
        Returns:
            AdminMenu: 创建的菜单
        """
        # 检查路由名称是否重复
        stmt = select(AdminMenu).where(
            AdminMenu.name == menu_data["name"],
            AdminMenu.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        existing_menu = result.scalar_one_or_none()
        if existing_menu:
            raise BusinessException(f"路由名称 {menu_data['name']} 已存在")
        
        # 创建菜单
        menu = AdminMenu(**menu_data)
        db.add(menu)
        await db.commit()
        await db.refresh(menu)
        
        return menu
    
    @staticmethod
    async def update_menu(db: AsyncSession, menu_id: int, menu_data: dict) -> AdminMenu:
        """
        更新菜单
        
        Args:
            db: 数据库会话
            menu_id: 菜单 ID
            menu_data: 菜单数据
            
        Returns:
            AdminMenu: 更新后的菜单
        """
        menu = await MenuService.get_menu_by_id(db, menu_id)
        if not menu:
            raise NotFoundException("菜单不存在")
        
        # 检查路由名称是否重复
        if "name" in menu_data and menu_data["name"] != menu.name:
            stmt = select(AdminMenu).where(
                AdminMenu.name == menu_data["name"],
                AdminMenu.deleted_at.is_(None)
            )
            result = await db.execute(stmt)
            existing_menu = result.scalar_one_or_none()
            if existing_menu:
                raise BusinessException(f"路由名称 {menu_data['name']} 已存在")
        
        # 更新菜单
        for key, value in menu_data.items():
            if value is not None:
                setattr(menu, key, value)
        
        await db.commit()
        await db.refresh(menu)
        
        return menu
    
    @staticmethod
    async def delete_menu(db: AsyncSession, menu_id: int) -> None:
        """
        删除菜单(软删除,级联删除子菜单)
        
        Args:
            db: 数据库会话
            menu_id: 菜单 ID
        """
        menu = await MenuService.get_menu_by_id(db, menu_id)
        if not menu:
            raise NotFoundException("菜单不存在")
        
        # 获取所有子菜单 ID
        child_ids = await MenuService._get_all_child_ids(db, menu_id)
        child_ids.append(menu_id)
        
        # 软删除
        from datetime import datetime
        stmt = select(AdminMenu).where(AdminMenu.id.in_(child_ids))
        result = await db.execute(stmt)
        menus = result.scalars().all()
        
        for m in menus:
            m.deleted_at = datetime.utcnow()
        
        await db.commit()
    
    @staticmethod
    async def _get_all_child_ids(db: AsyncSession, parent_id: int) -> List[int]:
        """
        递归获取所有子菜单 ID
        
        Args:
            db: 数据库会话
            parent_id: 父菜单 ID
            
        Returns:
            List[int]: 子菜单 ID 列表
        """
        stmt = select(AdminMenu).where(
            AdminMenu.parent_id == parent_id,
            AdminMenu.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        children = result.scalars().all()
        
        child_ids = []
        for child in children:
            child_ids.append(child.id)
            # 递归获取子菜单的子菜单
            sub_child_ids = await MenuService._get_all_child_ids(db, child.id)
            child_ids.extend(sub_child_ids)
        
        return child_ids
    
    @staticmethod
    def _build_tree(menus: List[AdminMenu], parent_id: int) -> List[MenuTreeNode]:
        """
        构建菜单树
        
        Args:
            menus: 菜单列表
            parent_id: 父菜单 ID
            
        Returns:
            List[MenuTreeNode]: 菜单树
        """
        tree = []
        for menu in menus:
            if menu.parent_id == parent_id:
                node = MenuTreeNode.model_validate(menu)
                node.children = MenuService._build_tree(menus, menu.id)
                tree.append(node)
        
        return tree
    
    @staticmethod
    def _convert_to_routes(tree: List[MenuTreeNode]) -> List[MenuRoute]:
        """
        将菜单树转换为前端路由格式
        
        Args:
            tree: 菜单树
            
        Returns:
            List[MenuRoute]: 路由树
        """
        routes = []
        for node in tree:
            # 跳过隐藏的菜单
            if node.hidden == 1:
                continue
            
            route = MenuRoute(
                id=node.id,
                title=node.title,
                name=node.name,
                path=node.path or "",
                component=node.component or "",
                meta=MenuMeta(
                    icon=node.icon,
                    title=node.title,
                    hidden=bool(node.hidden),
                    keepAlive=bool(node.keep_alive)
                ),
                children=MenuService._convert_to_routes(node.children)
            )
            routes.append(route)
        
        return routes
