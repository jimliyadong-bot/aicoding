"""
全局异常处理
"""
from typing import Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class APIException(Exception):
    """API 自定义异常基类"""
    
    def __init__(
        self,
        code: int = 500,
        message: str = "Internal Server Error",
        data: Any = None
    ):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(self.message)


class BusinessException(APIException):
    """业务异常"""
    
    def __init__(self, message: str = "Business Error", data: Any = None):
        super().__init__(code=422, message=message, data=data)


class NotFoundException(APIException):
    """资源不存在异常"""
    
    def __init__(self, message: str = "Resource Not Found", data: Any = None):
        super().__init__(code=404, message=message, data=data)


class UnauthorizedException(APIException):
    """未认证异常"""
    
    def __init__(self, message: str = "Unauthorized", data: Any = None):
        super().__init__(code=401, message=message, data=data)


class ForbiddenException(APIException):
    """无权限异常"""
    
    def __init__(self, message: str = "Forbidden", data: Any = None):
        super().__init__(code=403, message=message, data=data)


class BadRequestException(APIException):
    """请求参数错误异常"""
    
    def __init__(self, message: str = "Bad Request", data: Any = None):
        super().__init__(code=400, message=message, data=data)


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """
    API 异常处理器
    
    Args:
        request: 请求对象
        exc: 异常对象
        
    Returns:
        JSONResponse: 统一格式的错误响应
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    return JSONResponse(
        status_code=exc.code if exc.code < 500 else 500,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": exc.data,
            "trace_id": trace_id
        }
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException
) -> JSONResponse:
    """
    HTTP 异常处理器
    
    Args:
        request: 请求对象
        exc: HTTP 异常对象
        
    Returns:
        JSONResponse: 统一格式的错误响应
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None,
            "trace_id": trace_id
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    参数验证异常处理器
    
    Args:
        request: 请求对象
        exc: 验证异常对象
        
    Returns:
        JSONResponse: 统一格式的错误响应
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 格式化验证错误信息
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "message": "参数验证失败",
            "data": {"errors": errors},
            "trace_id": trace_id
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    通用异常处理器(捕获所有未处理的异常)
    
    Args:
        request: 请求对象
        exc: 异常对象
        
    Returns:
        JSONResponse: 统一格式的错误响应
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 记录异常日志
    import traceback
    print(f"[ERROR] Trace ID: {trace_id}")
    print(f"[ERROR] Exception: {exc}")
    print(traceback.format_exc())
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None,
            "trace_id": trace_id
        }
    )
