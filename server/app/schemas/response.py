"""
统一响应模型
"""
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    """统一响应模型"""
    code: int = Field(description="状态码")
    message: str = Field(description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    trace_id: str = Field(description="请求追踪ID")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": None,
                "trace_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class PageData(BaseModel, Generic[T]):
    """分页数据模型"""
    items: list[T] = Field(description="数据列表")
    total: int = Field(description="总记录数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页数量")
    total_pages: int = Field(description="总页数")

    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "total_pages": 5
            }
        }


def success_response(
    data: Any = None,
    message: str = "success",
    trace_id: str = ""
) -> dict:
    """
    成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        trace_id: 请求追踪ID
        
    Returns:
        dict: 统一响应格式
    """
    return {
        "code": 200,
        "message": message,
        "data": data,
        "trace_id": trace_id
    }


def error_response(
    code: int = 500,
    message: str = "Internal Server Error",
    data: Any = None,
    trace_id: str = ""
) -> dict:
    """
    错误响应
    
    Args:
        code: 错误码
        message: 错误消息
        data: 错误详情
        trace_id: 请求追踪ID
        
    Returns:
        dict: 统一响应格式
    """
    return {
        "code": code,
        "message": message,
        "data": data,
        "trace_id": trace_id
    }
