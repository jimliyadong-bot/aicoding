"""
初始化权限和角色脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.role import AdminRole
from app.models.permission import AdminPermission
from app.models.user import AdminUser
from app.models.menu import AdminMenu  # 添加菜单模型导入


async def seed_roles():
    """初始化角色"""
    async with AsyncSessionLocal() as db:
        try:
            # 检查是否已存在角色
            stmt = select(AdminRole)
            result = await db.execute(stmt)
            existing_roles = result.scalars().all()
            
            if existing_roles:
                print("✅ 角色已存在,跳过创建")
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
            
            print("✅ 角色创建成功!")
            for role in roles:
                print(f"   - {role.name} ({role.code})")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ 创建角色失败: {str(e)}")
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
                print("✅ 权限已存在,跳过创建")
                return
            
            # 创建权限
            permissions = [
                # 用户管理权限
                AdminPermission(name="查看用户列表", code="sys:user:list", type="API", description="查看用户列表"),
                AdminPermission(name="创建用户", code="sys:user:create", type="API", description="创建新用户"),
                AdminPermission(name="更新用户", code="sys:user:update", type="API", description="更新用户信息"),
                AdminPermission(name="删除用户", code="sys:user:delete", type="API", description="删除用户"),
                
                # 角色管理权限
                AdminPermission(name="查看角色列表", code="sys:role:list", type="API", description="查看角色列表"),
                AdminPermission(name="创建角色", code="sys:role:create", type="API", description="创建新角色"),
                AdminPermission(name="更新角色", code="sys:role:update", type="API", description="更新角色信息"),
                AdminPermission(name="删除角色", code="sys:role:delete", type="API", description="删除角色"),
                AdminPermission(name="分配权限", code="sys:role:assign", type="API", description="给角色分配权限"),
                
                # 权限管理权限
                AdminPermission(name="查看权限列表", code="sys:permission:list", type="API", description="查看权限列表"),
                AdminPermission(name="创建权限", code="sys:permission:create", type="API", description="创建新权限"),
                AdminPermission(name="更新权限", code="sys:permission:update", type="API", description="更新权限信息"),
                AdminPermission(name="删除权限", code="sys:permission:delete", type="API", description="删除权限"),
                
                # 菜单管理权限
                AdminPermission(name="查看菜单列表", code="sys:menu:list", type="API", description="查看菜单列表"),
                AdminPermission(name="创建菜单", code="sys:menu:create", type="API", description="创建新菜单"),
                AdminPermission(name="更新菜单", code="sys:menu:update", type="API", description="更新菜单信息"),
                AdminPermission(name="删除菜单", code="sys:menu:delete", type="API", description="删除菜单"),
                
                # 示例权限
                AdminPermission(name="查看示例", code="sys:demo:view", type="API", description="查看示例接口"),
                AdminPermission(name="示例列表", code="sys:demo:list", type="API", description="示例列表接口"),
            ]
            
            db.add_all(permissions)
            await db.commit()
            
            print("✅ 权限创建成功!")
            print(f"   共创建 {len(permissions)} 个权限")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ 创建权限失败: {str(e)}")
            raise


async def assign_super_admin_role():
    """给管理员用户分配超级管理员角色"""
    async with AsyncSessionLocal() as db:
        try:
            # 查询管理员用户
            user_stmt = select(AdminUser).where(AdminUser.username == "admin")
            user_result = await db.execute(user_stmt)
            admin_user = user_result.scalar_one_or_none()
            
            if not admin_user:
                print("⚠️  管理员用户不存在,请先运行 seed_admin.py")
                return
            
            # 查询超级管理员角色
            role_stmt = select(AdminRole).where(AdminRole.code == "SUPER_ADMIN")
            role_result = await db.execute(role_stmt)
            super_admin_role = role_result.scalar_one_or_none()
            
            if not super_admin_role:
                print("⚠️  超级管理员角色不存在")
                return
            
            # 检查是否已分配
            if super_admin_role in admin_user.roles:
                print("✅ 管理员已拥有超级管理员角色")
                return
            
            # 分配角色
            admin_user.roles.append(super_admin_role)
            await db.commit()
            
            print("✅ 超级管理员角色分配成功!")
            print(f"   用户: {admin_user.username}")
            print(f"   角色: {super_admin_role.name} ({super_admin_role.code})")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ 分配角色失败: {str(e)}")
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
    print("\n[3/3] 分配超级管理员角色...")
    await assign_super_admin_role()
    
    print("\n" + "=" * 50)
    print("✅ 初始化完成!")
    print("=" * 50)
    print("\n提示:")
    print("  - 超级管理员拥有所有权限(无需绑定)")
    print("  - 其他角色需要手动绑定权限")
    print("  - 使用 sys:module:action 格式的权限编码")


if __name__ == "__main__":
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
