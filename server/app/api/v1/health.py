"""
健康检查路由
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
from app.db.redis import redis_client
from app.schemas.response import success_response

router = APIRouter()


@router.get("/health")
async def health_check(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    健康检查接口
    
    检查服务状态、数据库连接和 Redis 连接
    
    Returns:
        dict: 健康检查结果
    """
    trace_id = getattr(request.state, "trace_id", "")
    
    # 检查数据库连接
    try:
        await db.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception as e:
        database_status = f"error: {str(e)}"
    
    # 检查 Redis 连接
    try:
        await redis_client.ping()
        redis_status = "connected"
    except Exception as e:
        redis_status = f"error: {str(e)}"
    
    # 返回健康检查结果
    data = {
        "status": "healthy" if database_status == "connected" and redis_status == "connected" else "unhealthy",
        "database": database_status,
        "redis": redis_status
    }
    
    return success_response(data=data, trace_id=trace_id)
