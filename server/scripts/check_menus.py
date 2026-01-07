"""
查看菜单数据
"""
import asyncio
import sys
from sqlalchemy import select
from app.db.session import get_db
from app.models.menu import AdminMenu

async def main():
    async for db in get_db():
        result = await db.execute(
            select(AdminMenu)
            .where(AdminMenu.deleted_at.is_(None))
            .order_by(AdminMenu.sort, AdminMenu.id)
        )
        menus = result.scalars().all()
        
        print("=== 菜单数据 ===")
        for m in menus:
            print(f"ID:{m.id} | Name:{m.name} | Path:{m.path} | Component:{m.component} | ParentID:{m.parent_id}")
        break

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
