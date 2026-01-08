"""
配置管理模块
"""
from typing import List
from urllib.parse import urlsplit
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用配置
    APP_NAME: str = "YiYa AI Reader"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    DATABASE_URL: str = Field(
        ...,
        description="数据库连接URL"
    )
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    
    @property
    def REDIS_URL(self) -> str:
        """Redis 连接 URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # JWT 配置
    SECRET_KEY: str = Field(
        ...,
        description="JWT密钥"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS 配置(字符串,内部转换为列表)
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """返回 CORS 允许的源列表"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    # Trace ID 配置
    TRACE_ID_HEADER: str = "X-Trace-ID"
    
    # 微信小程序配置
    WECHAT_APPID: str = ""
    WECHAT_SECRET: str = ""

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("SECRET_KEY 不能为空")
        normalized = value.strip()
        if normalized in {"your-secret-key-change-this-in-production", "your-secret-key-here"}:
            raise ValueError("SECRET_KEY 不能使用默认占位值")
        return normalized

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("DATABASE_URL 不能为空")
        normalized = value.strip()
        parsed = urlsplit(normalized)
        if parsed.username is not None and (parsed.password is None or parsed.password == ""):
            raise ValueError("DATABASE_URL 必须包含数据库密码")
        if ":password@" in normalized or "root:password@" in normalized:
            raise ValueError("DATABASE_URL 不能使用默认密码")
        return normalized
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()

