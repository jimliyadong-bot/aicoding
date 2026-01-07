"""
审计日志模型
"""
from sqlalchemy import String, BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel


class AdminAuditLog(BaseModel):
    """管理端审计日志模型"""
    
    __tablename__ = "admin_audit_log"
    
    actor_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="操作人ID"
    )
    
    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="操作类型: CREATE/UPDATE/DELETE"
    )
    
    target_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="目标类型: USER/ROLE/PERMISSION/MENU"
    )
    
    target_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
        comment="目标ID"
    )
    
    diff: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="变更内容(JSON)"
    )
    
    ip: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="IP地址"
    )
    
    user_agent: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="User Agent"
    )
    
    def __repr__(self) -> str:
        return f"<AdminAuditLog(id={self.id}, actor_id={self.actor_id}, action={self.action}, target_type={self.target_type})>"
