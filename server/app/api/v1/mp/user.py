"""
小程序用户路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.mp_user import MiniProgramUser
from app.schemas.mp_user import MiniProgramUserInfo, UpdateUserInfoRequest
from app.schemas.response import success_response
from app.core.dependencies import get_current_mp_user

router = APIRouter()


@router.get("/me", response_model=dict)
async def get_current_user_info(
    request: Request,
    current_user: MiniProgramUser = Depends(get_current_mp_user)
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
    
    user_info = MiniProgramUserInfo.model_validate(current_user)
    
    return success_response(
        data=user_info.model_dump(),
        trace_id=trace_id
    )


@router.put("/me", response_model=dict)
async def update_current_user_info(
    request: Request,
    update_data: UpdateUserInfoRequest,
    current_user: MiniProgramUser = Depends(get_current_mp_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户信息
    
    Args:
        request: 请求对象
        update_data: 更新数据
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 更新后的用户信息
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 更新用户信息
    if update_data.nickname is not None:
        current_user.nickname = update_data.nickname
    if update_data.avatar is not None:
        current_user.avatar = update_data.avatar
    
    await db.commit()
    await db.refresh(current_user)
    
    user_info = MiniProgramUserInfo.model_validate(current_user)
    
    return success_response(
        data=user_info.model_dump(),
        message="更新成功",
        trace_id=trace_id
    )
