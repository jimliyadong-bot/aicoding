"""
错误码定义
"""
from enum import Enum


class ErrorCode(Enum):
    """错误码枚举"""
    
    # 成功
    SUCCESS = (200, "成功")
    
    # 客户端错误 (400xx)
    BAD_REQUEST = (40000, "请求参数错误")
    UNAUTHORIZED = (40001, "用户名或密码错误")
    INVALID_TOKEN = (40002, "Token无效或过期")
    FORBIDDEN = (40003, "无权限访问")
    NOT_FOUND = (40004, "资源不存在")
    USER_EXISTS = (40005, "用户已存在")
    ROLE_EXISTS = (40006, "角色已存在")
    MENU_EXISTS = (40007, "菜单已存在")
    PERMISSION_EXISTS = (40008, "权限已存在")
    
    # 服务器错误 (500xx)
    INTERNAL_ERROR = (50000, "服务器内部错误")
    DATABASE_ERROR = (50001, "数据库错误")
    REDIS_ERROR = (50002, "Redis错误")
    
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


# 错误码映射
ERROR_CODE_MAP = {
    error.code: error.message
    for error in ErrorCode
}


def get_error_message(code: int) -> str:
    """
    获取错误消息
    
    Args:
        code: 错误码
        
    Returns:
        str: 错误消息
    """
    return ERROR_CODE_MAP.get(code, "未知错误")
