"""
审计日志工具
"""
import json
from functools import wraps
from typing import Callable, Any
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AdminAuditLog
from app.models.user import AdminUser


def get_client_ip(request: Request) -> str:
    """获取客户端 IP"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> str:
    """获取 User Agent"""
    return request.headers.get("User-Agent", "unknown")


async def create_audit_log(
    db: AsyncSession,
    actor_id: int,
    action: str,
    target_type: str,
    target_id: int | None = None,
    diff: dict | None = None,
    ip: str | None = None,
    user_agent: str | None = None
):
    """
    创建审计日志
    
    Args:
        db: 数据库会话
        actor_id: 操作人ID
        action: 操作类型
        target_type: 目标类型
        target_id: 目标ID
        diff: 变更内容
        ip: IP地址
        user_agent: User Agent
    """
    audit_log = AdminAuditLog(
        actor_id=actor_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        diff=json.dumps(diff, ensure_ascii=False) if diff else None,
        ip=ip,
        user_agent=user_agent
    )
    db.add(audit_log)
    await db.commit()


def audit_log(action: str, target_type: str):
    """
    审计日志装饰器
    
    Args:
        action: 操作类型(CREATE/UPDATE/DELETE)
        target_type: 目标类型(USER/ROLE/PERMISSION/MENU)
    
    Usage:
        @audit_log(action="CREATE", target_type="USER")
        async def create_user(...):
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 执行原函数
            result = await func(*args, **kwargs)
            
            # 尝试记录审计日志
            try:
                # 从参数中获取 request, db, current_user
                request: Request | None = None
                db: AsyncSession | None = None
                current_user: AdminUser | None = None
                target_id: int | None = None
                diff: dict | None = None
                
                # 从 kwargs 中提取
                if "request" in kwargs:
                    request = kwargs["request"]
                if "db" in kwargs:
                    db = kwargs["db"]
                if "current_user" in kwargs:
                    current_user = kwargs["current_user"]
                
                # 从 args 中提取(根据函数签名)
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                    elif isinstance(arg, AsyncSession):
                        db = arg
                    elif isinstance(arg, AdminUser):
                        current_user = arg
                
                # 获取 target_id
                if action in ["UPDATE", "DELETE"]:
                    # 从路径参数中获取 ID
                    if "id" in kwargs:
                        target_id = kwargs["id"]
                    elif "user_id" in kwargs:
                        target_id = kwargs["user_id"]
                    elif "role_id" in kwargs:
                        target_id = kwargs["role_id"]
                    elif "menu_id" in kwargs:
                        target_id = kwargs["menu_id"]
                elif action == "CREATE":
                    # 从返回结果中获取 ID
                    if hasattr(result, "id"):
                        target_id = result.id
                
                # 记录审计日志
                if db and current_user:
                    await create_audit_log(
                        db=db,
                        actor_id=current_user.id,
                        action=action,
                        target_type=target_type,
                        target_id=target_id,
                        diff=diff,
                        ip=get_client_ip(request) if request else None,
                        user_agent=get_user_agent(request) if request else None
                    )
            except Exception as e:
                # 审计日志失败不影响主流程
                print(f"审计日志记录失败: {e}")
            
            return result
        
        return wrapper
    return decorator
