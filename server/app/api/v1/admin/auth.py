"""
管理端认证路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    LogoutRequest,
    UserInfoResponse
)
from app.schemas.response import success_response
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.models.user import AdminUser

router = APIRouter()


@router.post("/login", response_model=dict)
async def login(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    管理员登录
    
    Args:
        request: 请求对象
        login_data: 登录数据
        db: 数据库会话
        
    Returns:
        dict: Token 响应
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 获取客户端 IP
    ip_address = request.client.host if request.client else ""
    
    # 执行登录
    token_response = await AuthService.login(
        db=db,
        username=login_data.username,
        password=login_data.password,
        ip_address=ip_address
    )
    
    return success_response(
        data=token_response.model_dump(),
        message="登录成功",
        trace_id=trace_id
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    request: Request,
    refresh_data: RefreshTokenRequest
):
    """
    刷新 Access Token
    
    Args:
        request: 请求对象
        refresh_data: 刷新数据
        
    Returns:
        dict: 新的 Access Token
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 刷新 Token
    token_response = await AuthService.refresh_access_token(
        refresh_token=refresh_data.refresh_token
    )
    
    return success_response(
        data=token_response.model_dump(),
        message="Token 刷新成功",
        trace_id=trace_id
    )


@router.get("/me", response_model=dict)
async def get_current_user_info(
    request: Request,
    current_user: AdminUser = Depends(get_current_user)
):
    """
    获取当前用户信息
    
    Args:
        request: 请求对象
        current_user: 当前用户
        
    Returns:
        dict: 用户信息
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 构建用户信息响应
    user_info = UserInfoResponse.model_validate(current_user)
    
    return success_response(
        data=user_info.model_dump(),
        message="获取用户信息成功",
        trace_id=trace_id
    )


@router.post("/logout", response_model=dict)
async def logout(
    request: Request,
    logout_data: LogoutRequest,
    current_user: AdminUser = Depends(get_current_user)
):
    """
    用户登出
    
    Args:
        request: 请求对象
        logout_data: 登出数据
        current_user: 当前用户
        
    Returns:
        dict: 登出响应
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 执行登出
    await AuthService.logout(
        user_id=current_user.id,
        refresh_token=logout_data.refresh_token
    )
    
    return success_response(
        data=None,
        message="登出成功",
        trace_id=trace_id
    )
