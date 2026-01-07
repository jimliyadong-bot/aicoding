"""
FastAPI 应用入口
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.db.redis import redis_client
from app.core.exceptions import (
    APIException,
    api_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from app.middleware.trace_id import TraceIDMiddleware
from app.api.v1 import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    await redis_client.connect()
    print("✅ Redis 连接成功")
    
    yield
    
    # 关闭时执行
    await redis_client.close()
    print("✅ Redis 连接已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加 Trace ID 中间件
app.add_middleware(TraceIDMiddleware, header_name=getattr(settings, "TRACE_ID_HEADER", "X-Trace-ID"))

# 注册全局异常处理器
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/")
async def root():
    """根路径"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


# 注册路由
app.include_router(health.router, prefix="/api/v1", tags=["健康检查"])

# 管理端路由
from app.api.v1.admin import auth as admin_auth, demo as admin_demo, menu as admin_menu
from app.api.v1.admin import user as admin_user, role as admin_role, permission as admin_permission
app.include_router(admin_auth.router, prefix="/api/v1/admin/auth", tags=["管理端-认证"])
app.include_router(admin_demo.router, prefix="/api/v1/admin/demo", tags=["管理端-示例"])
app.include_router(admin_menu.router, prefix="/api/v1/admin/menus", tags=["管理端-菜单"])
app.include_router(admin_user.router, prefix="/api/v1/admin/users", tags=["管理端-用户"])
app.include_router(admin_role.router, prefix="/api/v1/admin/roles", tags=["管理端-角色"])
app.include_router(admin_permission.router, prefix="/api/v1/admin/permissions", tags=["管理端-权限"])

# 小程序路由
from app.api.v1.mp import auth as mp_auth, user as mp_user
app.include_router(mp_auth.router, prefix="/api/v1/mp/auth", tags=["小程序-认证"])
app.include_router(mp_user.router, prefix="/api/v1/mp/user", tags=["小程序-用户"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
