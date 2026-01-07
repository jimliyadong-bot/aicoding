"""
初始化菜单脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.menu import AdminMenu
from app.models.role import AdminRole
from app.models.user import AdminUser
from app.models.permission import AdminPermission


async def seed_menus():
    """初始化菜单"""
    async with AsyncSessionLocal() as db:
        try:
            # 检查是否已存在菜单
            stmt = select(AdminMenu)
            result = await db.execute(stmt)
            existing_menus = result.scalars().all()
            
            if existing_menus:
                print("✅ 菜单已存在,跳过创建")
                return
            
            # 创建菜单
            menus = [
                # 一级菜单
                AdminMenu(
                    id=1,
                    parent_id=0,
                    title="仪表盘",
                    name="Dashboard",
                    path="/dashboard",
                    component="views/dashboard/index.vue",
                    icon="Dashboard",
                    sort=1,
                    hidden=0,
                    keep_alive=1,
                    status=1
                ),
                AdminMenu(
                    id=2,
                    parent_id=0,
                    title="系统管理",
                    name="System",
                    path="/system",
                    component="Layout",
                    icon="Setting",
                    sort=2,
                    hidden=0,
                    keep_alive=1,
                    status=1
                ),
                
                # 系统管理子菜单
                AdminMenu(
                    id=10,
                    parent_id=2,
                    title="用户管理",
                    name="User",
                    path="/system/user",
                    component="views/system/user/index.vue",
                    icon="User",
                    sort=1,
                    hidden=0,
                    keep_alive=1,
                    status=1
                ),
                AdminMenu(
                    id=11,
                    parent_id=2,
                    title="角色管理",
                    name="Role",
                    path="/system/role",
                    component="views/system/role/index.vue",
                    icon="UserFilled",
                    sort=2,
                    hidden=0,
                    keep_alive=1,
                    status=1
                ),
                AdminMenu(
                    id=12,
                    parent_id=2,
                    title="权限管理",
                    name="Permission",
                    path="/system/permission",
                    component="views/system/permission/index.vue",
                    icon="Lock",
                    sort=3,
                    hidden=0,
                    keep_alive=1,
                    status=1
                ),
                AdminMenu(
                    id=13,
                    parent_id=2,
                    title="菜单管理",
                    name="Menu",
                    path="/system/menu",
                    component="views/system/menu/index.vue",
                    icon="Menu",
                    sort=4,
                    hidden=0,
                    keep_alive=1,
                    status=1
                ),
            ]
            
            db.add_all(menus)
            await db.commit()
            
            print("✅ 菜单创建成功!")
            print(f"   共创建 {len(menus)} 个菜单")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ 创建菜单失败: {str(e)}")
            raise


async def assign_menus_to_roles():
    """给角色分配菜单"""
    async with AsyncSessionLocal() as db:
        try:
            # 查询超级管理员角色
            super_admin_stmt = select(AdminRole).where(AdminRole.code == "SUPER_ADMIN")
            super_admin_result = await db.execute(super_admin_stmt)
            super_admin_role = super_admin_result.scalar_one_or_none()
            
            # 查询所有菜单
            menus_stmt = select(AdminMenu)
            menus_result = await db.execute(menus_stmt)
            all_menus = menus_result.scalars().all()
            
            if super_admin_role and all_menus:
                # 超级管理员拥有所有菜单
                super_admin_role.menus = all_menus
                await db.commit()
                print("✅ 超级管理员菜单分配成功!")
                print(f"   分配 {len(all_menus)} 个菜单")
            
            # 查询普通管理员角色
            admin_stmt = select(AdminRole).where(AdminRole.code == "ADMIN")
            admin_result = await db.execute(admin_stmt)
            admin_role = admin_result.scalar_one_or_none()
            
            if admin_role:
                # 普通管理员拥有部分菜单(仪表盘 + 系统管理的部分子菜单)
                admin_menus = [m for m in all_menus if m.id in [1, 2, 10, 11]]
                admin_role.menus = admin_menus
                await db.commit()
                print("✅ 普通管理员菜单分配成功!")
                print(f"   分配 {len(admin_menus)} 个菜单")
            
            # 查询普通用户角色
            user_stmt = select(AdminRole).where(AdminRole.code == "USER")
            user_result = await db.execute(user_stmt)
            user_role = user_result.scalar_one_or_none()
            
            if user_role:
                # 普通用户只有仪表盘
                user_menus = [m for m in all_menus if m.id == 1]
                user_role.menus = user_menus
                await db.commit()
                print("✅ 普通用户菜单分配成功!")
                print(f"   分配 {len(user_menus)} 个菜单")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ 分配菜单失败: {str(e)}")
            raise


async def main():
    """主函数"""
    print("=" * 50)
    print("开始初始化菜单...")
    print("=" * 50)
    
    # 1. 创建菜单
    print("\n[1/2] 创建菜单...")
    await seed_menus()
    
    # 2. 分配菜单到角色
    print("\n[2/2] 分配菜单到角色...")
    await assign_menus_to_roles()
    
    print("\n" + "=" * 50)
    print("✅ 初始化完成!")
    print("=" * 50)
    print("\n提示:")
    print("  - 超级管理员拥有所有菜单")
    print("  - 普通管理员拥有部分菜单")
    print("  - 普通用户只有仪表盘")


if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
