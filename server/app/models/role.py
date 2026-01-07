"""
角色模型
"""
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import SoftDeleteModel
from app.models.associations import admin_user_role, admin_role_permission, admin_role_menu


class AdminRole(SoftDeleteModel):
    """管理端角色模型"""
    
    __tablename__ = "admin_role"
    
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="角色名称"
    )
    
    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="角色编码(如: SUPER_ADMIN)"
    )
    
    description: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="角色描述"
    )
    
    status: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment="状态: 0-禁用, 1-启用"
    )
    
    # 关联关系
    permissions: Mapped[list["AdminPermission"]] = relationship(
        "AdminPermission",
        secondary=admin_role_permission,
        back_populates="roles",
        lazy="selectin"
    )
    
    users: Mapped[list["AdminUser"]] = relationship(
        "AdminUser",
        secondary=admin_user_role,
        back_populates="roles",
        lazy="selectin"
    )
    
    menus: Mapped[list["AdminMenu"]] = relationship(
        "AdminMenu",
        secondary=admin_role_menu,
        back_populates="roles",
        lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<AdminRole(id={self.id}, code={self.code}, name={self.name})>"
