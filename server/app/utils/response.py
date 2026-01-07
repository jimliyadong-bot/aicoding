"""
统一响应工具
"""
from typing import Any, Optional, Dict
from datetime import datetime
from fastapi.responses import JSONResponse


class ResponseCode:
    """响应状态码"""
    SUCCESS = 200
    BAD_REQUEST = 40000
    UNAUTHORIZED = 40001
    INVALID_TOKEN = 40002
    FORBIDDEN = 40003
    NOT_FOUND = 40004
    USER_EXISTS = 40005
    ROLE_EXISTS = 40006
    MENU_EXISTS = 40007
    INTERNAL_ERROR = 50000
    DATABASE_ERROR = 50001
    REDIS_ERROR = 50002


def success_response(
    data: Any = None,
    message: str = "success",
    code: int = ResponseCode.SUCCESS
) -> Dict[str, Any]:
    """
    成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 响应码
        
    Returns:
        Dict[str, Any]: 响应字典
    """
    return {
        "code": code,
        "message": message,
        "data": data,
        "timestamp": int(datetime.now().timestamp())
    }


def error_response(
    message: str,
    code: int = ResponseCode.INTERNAL_ERROR,
    data: Any = None
) -> Dict[str, Any]:
    """
    错误响应
    
    Args:
        message: 错误消息
        code: 错误码
        data: 额外数据
        
    Returns:
        Dict[str, Any]: 响应字典
    """
    return {
        "code": code,
        "message": message,
        "data": data,
        "timestamp": int(datetime.now().timestamp())
    }


def paginated_response(
    items: list,
    total: int,
    page: int,
    page_size: int,
    message: str = "success"
) -> Dict[str, Any]:
    """
    分页响应
    
    Args:
        items: 数据列表
        total: 总数
        page: 当前页
        page_size: 每页数量
        message: 响应消息
        
    Returns:
        Dict[str, Any]: 响应字典
    """
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "code": ResponseCode.SUCCESS,
        "message": message,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        },
        "timestamp": int(datetime.now().timestamp())
    }
