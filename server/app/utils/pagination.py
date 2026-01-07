"""
分页工具
"""
from typing import TypeVar, Generic, List
from pydantic import BaseModel


T = TypeVar('T')


class PaginationParams(BaseModel):
    """分页参数"""
    page: int = 1
    page_size: int = 20
    sort_by: str = "id"
    order: str = "desc"
    
    def get_offset(self) -> int:
        """获取偏移量"""
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """获取限制数量"""
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        """
        创建分页响应
        
        Args:
            items: 数据列表
            total: 总数
            page: 当前页
            page_size: 每页数量
            
        Returns:
            PaginatedResponse: 分页响应对象
        """
        total_pages = (total + page_size - 1) // page_size
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
