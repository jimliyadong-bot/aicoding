"""
重置数据库脚本 - 删除所有表并重新创建
"""
import asyncio
import sys
sys.path.insert(0, '.')

from app.db.session import engine
from app.models.base import Base
# 导入所有模型
from app.models.user import AdminUser
from app.models.role import AdminRole
from app.models.permission import AdminPermission
from app.models.menu import AdminMenu
from app.models.mp_user import MiniProgramUser
from app.models.audit_log import AdminAuditLog
from app.models.associations import admin_user_role, admin_role_permission, admin_role_menu


async def reset_database():
    """删除所有表并重新创建"""
    async with engine.begin() as conn:
        print("正在删除所有表...")
        await conn.run_sync(Base.metadata.drop_all)
        print("✅ 所有表已删除")
        
        print("\n正在创建所有表...")
        await conn.run_sync(Base.metadata.create_all)
        print("✅ 所有表已创建")
    
    await engine.dispose()
    print("\n✅ 数据库重置完成!")


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(reset_database())
