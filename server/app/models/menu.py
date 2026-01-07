"""
菜单模型
"""
from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import SoftDeleteModel
from app.models.associations import admin_role_menu


class AdminMenu(SoftDeleteModel):
    """管理端菜单模型"""
    
    __tablename__ = "admin_menu"
    
    parent_id: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        comment="父菜单ID(0为根节点)"
    )
    
    title: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="菜单标题"
    )
    
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="路由名称(唯一)"
    )
    
    path: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="路由路径"
    )
    
    component: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        comment="组件路径"
    )
    
    icon: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="菜单图标"
    )
    
    sort: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="排序号(升序)"
    )
    
    hidden: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="是否隐藏: 0-显示, 1-隐藏"
    )
    
    keep_alive: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment="是否缓存: 0-不缓存, 1-缓存"
    )
    
    status: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment="状态: 0-禁用, 1-启用"
    )
    
    # 关联关系
    roles: Mapped[list["AdminRole"]] = relationship(
        "AdminRole",
        secondary=admin_role_menu,
        back_populates="menus",
        lazy="selectin"
    )

    
    def __repr__(self) -> str:
        return f"<AdminMenu(id={self.id}, name={self.name}, title={self.title})>"
