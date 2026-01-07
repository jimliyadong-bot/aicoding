"""
权限模型
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel
from app.models.associations import admin_role_permission


class AdminPermission(BaseModel):
    """管理端权限模型"""
    
    __tablename__ = "admin_permission"
    
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="权限名称"
    )
    
    code: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment="权限编码(如: sys:user:list)"
    )
    
    type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="权限类型: MENU-菜单, BUTTON-按钮, API-接口"
    )
    
    description: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="权限描述"
    )
    
    # 关联关系
    roles: Mapped[list["AdminRole"]] = relationship(
        "AdminRole",
        secondary=admin_role_permission,
        back_populates="permissions",
        lazy="selectin"
    )

    
    def __repr__(self) -> str:
        return f"<AdminPermission(id={self.id}, code={self.code})>"
