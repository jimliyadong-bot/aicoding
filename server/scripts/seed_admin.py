"""
初始化管理员账号脚本
"""
import asyncio
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.user import AdminUser
from app.models.role import AdminRole
from app.models.permission import AdminPermission
from app.models.menu import AdminMenu
from app.utils.password import hash_password


async def seed_admin():
    """初始化管理员账号"""
    async with AsyncSessionLocal() as db:
        try:
            # 检查是否已存在管理员
            stmt = select(AdminUser).where(AdminUser.username == "admin")
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print("✅ 管理员账号已存在,无需重复创建")
                print(f"   用户名: {existing_user.username}")
                print(f"   ID: {existing_user.id}")
                return
            
            # 创建管理员账号
            admin_user = AdminUser(
                username="admin",
                password_hash=hash_password("admin123"),
                real_name="超级管理员",
                status=1
            )
            
            db.add(admin_user)
            await db.commit()
            await db.refresh(admin_user)
            
            print("✅ 管理员账号创建成功!")
            print(f"   用户名: {admin_user.username}")
            print(f"   密码: admin123")
            print(f"   ID: {admin_user.id}")
            print("\n⚠️  请在生产环境中修改默认密码!")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ 创建管理员账号失败: {str(e)}")
            raise


if __name__ == "__main__":
    import sys
    print("开始初始化管理员账号...")
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_admin())
