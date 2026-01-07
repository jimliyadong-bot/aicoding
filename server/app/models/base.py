"""
数据库模型基类
"""
from datetime import datetime
from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """所有模型的基类"""
    pass


class BaseModel(Base):
    """
    通用模型基类
    
    包含所有表的通用字段:
    - id: 主键
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment="主键ID"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment="创建时间"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间"
    )


class SoftDeleteModel(BaseModel):
    """
    软删除模型基类
    
    在 BaseModel 基础上增加软删除字段:
    - deleted_at: 删除时间
    """
    __abstract__ = True
    
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
        comment="删除时间(软删除)"
    )
