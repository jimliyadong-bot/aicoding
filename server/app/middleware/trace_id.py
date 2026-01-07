"""
Trace ID 中间件
"""
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class TraceIDMiddleware(BaseHTTPMiddleware):
    """
    Trace ID 中间件
    
    为每个请求生成唯一的 trace_id,用于请求追踪和日志关联
    """
    
    def __init__(self, app, header_name: str = "X-Trace-ID"):
        super().__init__(app)
        self.header_name = header_name
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        处理请求
        
        Args:
            request: 请求对象
            call_next: 下一个中间件或路由处理器
            
        Returns:
            Response: 响应对象
        """
        # 从请求头获取 trace_id,如果没有则生成新的
        trace_id = request.headers.get(self.header_name)
        if not trace_id:
            trace_id = str(uuid.uuid4())
        
        # 将 trace_id 存储到请求状态中
        request.state.trace_id = trace_id
        
        # 调用下一个处理器
        response = await call_next(request)
        
        # 在响应头中返回 trace_id
        response.headers[self.header_name] = trace_id
        
        return response
