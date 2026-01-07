"""
小程序用户模型
"""
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import SoftDeleteModel


class MiniProgramUser(SoftDeleteModel):
    """小程序用户模型"""
    
    __tablename__ = "mp_user"
    
    openid: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        comment="微信 openid"
    )
    
    unionid: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="微信 unionid"
    )
    
    session_key: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="微信 session_key"
    )
    
    nickname: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="昵称"
    )
    
    avatar: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        comment="头像URL"
    )
    
    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="手机号"
    )
    
    gender: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
        comment="性别: 0-未知, 1-男, 2-女"
    )
    
    country: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="国家"
    )
    
    province: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="省份"
    )
    
    city: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="城市"
    )
    
    def __repr__(self) -> str:
        return f"<MiniProgramUser(id={self.id}, openid={self.openid}, nickname={self.nickname})>"
