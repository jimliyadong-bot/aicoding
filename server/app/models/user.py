"""
用户模型
"""
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import SoftDeleteModel
from app.models.associations import admin_user_role


class AdminUser(SoftDeleteModel):
    """管理端用户模型"""
    
    __tablename__ = "admin_user"
    
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="用户名"
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="密码哈希"
    )
    
    real_name: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="真实姓名"
    )
    
    phone: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
        comment="手机号"
    )
    
    email: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
        comment="邮箱"
    )
    
    avatar: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="头像URL"
    )
    
    status: Mapped[int] = mapped_column(
        Integer,
        default=1,
        comment="状态: 0-禁用, 1-启用"
    )
    
    last_login_at: Mapped[DateTime | None] = mapped_column(
        DateTime,
        nullable=True,
        comment="最后登录时间"
    )
    
    last_login_ip: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="最后登录IP"
    )
    
    # 关联关系
    roles: Mapped[list["AdminRole"]] = relationship(
        "AdminRole",
        secondary=admin_user_role,
        back_populates="users",
        lazy="selectin"
    )

    
    def __repr__(self) -> str:
        return f"<AdminUser(id={self.id}, username={self.username})>"
