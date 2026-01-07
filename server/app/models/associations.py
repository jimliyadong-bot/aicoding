"""
关联表模型
"""
from sqlalchemy import Table, Column, BigInteger, DateTime, ForeignKey, func
from app.models.base import Base

# 用户-角色关联表
admin_user_role = Table(
    "admin_user_role",
    Base.metadata,
    Column("user_id", BigInteger, ForeignKey("admin_user.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", BigInteger, ForeignKey("admin_role.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, server_default=func.now())
)

# 角色-权限关联表
admin_role_permission = Table(
    "admin_role_permission",
    Base.metadata,
    Column("role_id", BigInteger, ForeignKey("admin_role.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", BigInteger, ForeignKey("admin_permission.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, server_default=func.now())
)

# 角色-菜单关联表
admin_role_menu = Table(
    "admin_role_menu",
    Base.metadata,
    Column("role_id", BigInteger, ForeignKey("admin_role.id", ondelete="CASCADE"), primary_key=True),
    Column("menu_id", BigInteger, ForeignKey("admin_menu.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, server_default=func.now())
)
