"""
小程序认证路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.mp_user import MiniProgramUser
from app.schemas.mp_user import LoginByCodeRequest, LoginResponse, BindPhoneRequest, BindPhoneResponse
from app.schemas.response import success_response
from app.utils.wechat import wechat_mp
from app.core.dependencies import get_current_mp_user

router = APIRouter()


@router.post("/login_by_code", response_model=dict)
async def login_by_code(
    request: Request,
    login_data: LoginByCodeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    通过微信 code 登录
    
    Args:
        request: 请求对象
        login_data: 登录数据
        db: 数据库会话
        
    Returns:
        dict: 登录响应
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 调用微信接口换取 openid 和 session_key
    wx_data = await wechat_mp.code2session(login_data.code)
    openid = wx_data.get("openid")
    session_key = wx_data.get("session_key")
    unionid = wx_data.get("unionid")
    
    # 查询或创建用户
    stmt = select(MiniProgramUser).where(MiniProgramUser.openid == openid)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    is_new_user = False
    if not user:
        # 创建新用户
        user = MiniProgramUser(
            openid=openid,
            session_key=session_key,
            unionid=unionid,
            nickname="微信用户"
        )
        db.add(user)
        is_new_user = True
    else:
        # 更新 session_key
        user.session_key = session_key
        if unionid:
            user.unionid = unionid
    
    await db.commit()
    await db.refresh(user)
    
    # 生成 JWT token
    from app.utils.jwt import create_access_token, create_refresh_token
    access_token = create_access_token({"sub": str(user.id), "username": user.openid, "role": "mp"})
    refresh_token = create_refresh_token({"sub": str(user.id), "username": user.openid, "role": "mp"})
    
    # 返回响应
    return success_response(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": 7200,
            "is_new_user": is_new_user,
            "need_bind_phone": not user.phone
        },
        message="登录成功",
        trace_id=trace_id
    )


@router.post("/bind_phone", response_model=dict)
async def bind_phone(
    request: Request,
    bind_data: BindPhoneRequest,
    current_user: MiniProgramUser = Depends(get_current_mp_user),
    db: AsyncSession = Depends(get_db)
):
    """
    绑定手机号
    
    Args:
        request: 请求对象
        bind_data: 绑定数据
        current_user: 当前用户
        db: 数据库会话
        
    Returns:
        dict: 绑定响应
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 调用微信接口获取手机号
    phone_info = await wechat_mp.get_phone_number(bind_data.code)
    phone_number = phone_info.get("phoneNumber") or phone_info.get("purePhoneNumber")
    
    # 更新用户手机号
    current_user.phone = phone_number
    await db.commit()
    
    return success_response(
        data={"phone": phone_number},
        message="绑定成功",
        trace_id=trace_id
    )
