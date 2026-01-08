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
from app.utils.password import hash_password


async def seed_admin():
    """初始化管理员账号"""
    async with AsyncSessionLocal() as db:
        try:
            admin_username = os.environ.get("ADMIN_USERNAME")
            admin_password = os.environ.get("ADMIN_PASSWORD")
            admin_real_name = os.environ.get("ADMIN_REAL_NAME", "超级管理员")

            if not admin_username or not admin_password:
                raise RuntimeError("必须设置 ADMIN_USERNAME 和 ADMIN_PASSWORD 环境变量")

            # 检查是否已存在管理员
            stmt = select(AdminUser).where(AdminUser.username == admin_username)
            result = await db.execute(stmt)
            existing_user = result.scalar_one_or_none()

            if existing_user:
                print("管理员账号已存在,无需重复创建")
                print(f"   用户名: {existing_user.username}")
                print(f"   ID: {existing_user.id}")
                return

            # 创建管理员账号
            admin_user = AdminUser(
                username=admin_username,
                password_hash=hash_password(admin_password),
                real_name=admin_real_name,
                status=1
            )

            db.add(admin_user)
            await db.commit()
            await db.refresh(admin_user)

            print("管理员账号创建成功!")
            print(f"   用户名: {admin_user.username}")
            print(f"   ID: {admin_user.id}")
            print("   请妥善保管管理员凭据")

        except Exception as e:
            await db.rollback()
            print(f"创建管理员账号失败: {str(e)}")
            raise


if __name__ == "__main__":
    print("开始初始化管理员账号...")
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_admin())
