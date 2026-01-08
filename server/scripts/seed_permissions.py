"""
初始化权限和角色脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import AsyncSessionLocal
from app.models.role import AdminRole
from app.models.permission import AdminPermission
from app.models.user import AdminUser


async def seed_roles():
    """初始化角色"""
    async with AsyncSessionLocal() as db:
        try:
            # 检查是否已存在角色
            stmt = select(AdminRole)
            result = await db.execute(stmt)
            existing_roles = result.scalars().all()

            if existing_roles:
                print("角色已存在,跳过创建")
                return

            # 创建角色
            roles = [
                AdminRole(
                    id=1,
                    name="超级管理员",
                    code="SUPER_ADMIN",
                    description="拥有系统所有权限",
                    status=1
                ),
                AdminRole(
                    id=2,
                    name="管理员",
                    code="ADMIN",
                    description="拥有系统管理权限",
                    status=1
                ),
                AdminRole(
                    id=3,
                    name="普通用户",
                    code="USER",
                    description="普通用户权限",
                    status=1
                )
            ]

            db.add_all(roles)
            await db.commit()

            print("角色创建成功!")
            for role in roles:
                print(f"   - {role.name} ({role.code})")

        except Exception as e:
            await db.rollback()
            print(f"创建角色失败: {str(e)}")
            raise


async def seed_permissions():
    """初始化权限"""
    async with AsyncSessionLocal() as db:
        try:
            # 检查是否已存在权限
            stmt = select(AdminPermission)
            result = await db.execute(stmt)
            existing_perms = result.scalars().all()

            if existing_perms:
                print("权限已存在,跳过创建")
                return

            # 创建权限
            permissions = [
                # 菜单权限
                AdminPermission(name="系统管理", code="sys:manage", type="MENU", description="系统管理菜单"),
                AdminPermission(name="用户管理", code="sys:user:view", type="MENU", description="用户管理菜单"),
                AdminPermission(name="角色管理", code="sys:role:view", type="MENU", description="角色管理菜单"),
                AdminPermission(name="权限管理", code="sys:permission:view", type="MENU", description="权限管理菜单"),
                AdminPermission(name="菜单管理", code="sys:menu:view", type="MENU", description="菜单管理菜单"),
                AdminPermission(name="审计日志", code="sys:audit:view", type="MENU", description="审计日志菜单"),

                # 用户管理权限点
                AdminPermission(name="用户列表", code="sys:user:list", type="API", description="用户列表"),
                AdminPermission(name="用户详情", code="sys:user:detail", type="API", description="用户详情"),
                AdminPermission(name="创建用户", code="sys:user:create", type="BUTTON", description="创建用户"),
                AdminPermission(name="更新用户", code="sys:user:update", type="BUTTON", description="更新用户"),
                AdminPermission(name="删除用户", code="sys:user:delete", type="BUTTON", description="删除用户"),
                AdminPermission(name="重置密码", code="sys:user:reset", type="BUTTON", description="重置密码"),
                AdminPermission(name="分配角色", code="sys:user:assign:role", type="BUTTON", description="分配角色"),

                # 角色管理权限点
                AdminPermission(name="角色列表", code="sys:role:list", type="API", description="角色列表"),
                AdminPermission(name="角色详情", code="sys:role:detail", type="API", description="角色详情"),
                AdminPermission(name="创建角色", code="sys:role:create", type="BUTTON", description="创建角色"),
                AdminPermission(name="更新角色", code="sys:role:update", type="BUTTON", description="更新角色"),
                AdminPermission(name="删除角色", code="sys:role:delete", type="BUTTON", description="删除角色"),
                AdminPermission(name="分配权限", code="sys:role:assign:permission", type="BUTTON", description="分配权限"),
                AdminPermission(name="分配菜单", code="sys:role:assign:menu", type="BUTTON", description="分配菜单"),

                # 权限管理权限点
                AdminPermission(name="权限列表", code="sys:permission:list", type="API", description="权限列表"),
                AdminPermission(name="权限详情", code="sys:permission:detail", type="API", description="权限详情"),
                AdminPermission(name="创建权限", code="sys:permission:create", type="BUTTON", description="创建权限"),
                AdminPermission(name="更新权限", code="sys:permission:update", type="BUTTON", description="更新权限"),
                AdminPermission(name="删除权限", code="sys:permission:delete", type="BUTTON", description="删除权限"),

                # 菜单管理权限点
                AdminPermission(name="菜单列表", code="sys:menu:list", type="API", description="菜单列表"),
                AdminPermission(name="创建菜单", code="sys:menu:create", type="BUTTON", description="创建菜单"),
                AdminPermission(name="更新菜单", code="sys:menu:update", type="BUTTON", description="更新菜单"),
                AdminPermission(name="删除菜单", code="sys:menu:delete", type="BUTTON", description="删除菜单"),

                # 示例权限
                AdminPermission(name="示例查看", code="sys:demo:view", type="API", description="示例查看"),
                AdminPermission(name="示例列表", code="sys:demo:list", type="API", description="示例列表"),
            ]

            db.add_all(permissions)
            await db.commit()

            print("权限创建成功!")
            print(f"   共创建 {len(permissions)} 个权限")

        except Exception as e:
            await db.rollback()
            print(f"创建权限失败: {str(e)}")
            raise


async def assign_super_admin_role():
    """给管理员用户分配超级管理员角色"""
    async with AsyncSessionLocal() as db:
        try:
            admin_username = os.environ.get("ADMIN_USERNAME")
            if not admin_username:
                print("未设置 ADMIN_USERNAME,无法分配超级管理员角色")
                return

            # 查询管理员用户
            user_stmt = select(AdminUser).where(AdminUser.username == admin_username)
            user_result = await db.execute(user_stmt)
            admin_user = user_result.scalar_one_or_none()

            if not admin_user:
                print("管理员用户不存在,请先运行 seed_admin.py")
                return

            # 查询超级管理员角色
            role_stmt = select(AdminRole).where(AdminRole.code == "SUPER_ADMIN")
            role_result = await db.execute(role_stmt)
            super_admin_role = role_result.scalar_one_or_none()

            if not super_admin_role:
                print("超级管理员角色不存在")
                return

            # 检查是否已分配
            if super_admin_role in admin_user.roles:
                print("管理员已拥有超级管理员角色")
                return

            # 分配角色
            admin_user.roles.append(super_admin_role)
            await db.commit()

            print("超级管理员角色分配成功!")
            print(f"   用户: {admin_user.username}")
            print(f"   角色: {super_admin_role.name} ({super_admin_role.code})")

        except Exception as e:
            await db.rollback()
            print(f"分配角色失败: {str(e)}")
            raise


async def assign_permissions_to_super_admin():
    """给超级管理员角色分配全部权限"""
    async with AsyncSessionLocal() as db:
        try:
            role_stmt = select(AdminRole).options(selectinload(AdminRole.permissions)).where(AdminRole.code == "SUPER_ADMIN")
            role_result = await db.execute(role_stmt)
            super_admin_role = role_result.scalar_one_or_none()

            if not super_admin_role:
                print("超级管理员角色不存在")
                return

            perm_stmt = select(AdminPermission)
            perm_result = await db.execute(perm_stmt)
            permissions = perm_result.scalars().all()

            if not permissions:
                print("未找到权限,跳过分配")
                return

            super_admin_role.permissions = list(permissions)
            await db.commit()

            print("超级管理员权限分配成功!")
            print(f"   分配 {len(permissions)} 个权限")

        except Exception as e:
            await db.rollback()
            print(f"分配权限失败: {str(e)}")
            raise


async def main():
    """主函数"""
    print("=" * 50)
    print("开始初始化权限和角色...")
    print("=" * 50)

    # 1. 创建角色
    print("\n[1/3] 创建角色...")
    await seed_roles()

    # 2. 创建权限
    print("\n[2/3] 创建权限...")
    await seed_permissions()

    # 3. 分配超级管理员角色
    print("\n[3/4] 分配超级管理员角色...")
    await assign_super_admin_role()

    # 4. 分配超级管理员权限
    print("\n[4/4] 分配超级管理员权限...")
    await assign_permissions_to_super_admin()

    print("\n" + "=" * 50)
    print("初始化完成!")
    print("=" * 50)
    print("\n提示:")
    print("  - 超级管理员拥有所有权限(无需绑定)")
    print("  - 其他角色需要手动绑定权限")
    print("  - 使用 sys:module:action 格式的权限编码")


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
