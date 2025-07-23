"""Pydantic models for product data structures."""
from typing import Optional, List, Generic, TypeVar
from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    """Product model with all fields."""
    id: int
    name: str
    description: str
    price: float
    category: str
    tags: List[str] = []
    in_stock: bool = True
    created_at: datetime = datetime.now()


class ProductCreate(BaseModel):
    """Model for creating a new product."""
    name: str
    description: str
    price: float
    category: str
    tags: List[str] = []
    in_stock: bool = True


class ProductUpdate(BaseModel):
    """Model for updating an existing product."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    in_stock: Optional[bool] = None


class PaginationParams(BaseModel):
    """Model for pagination parameters."""
    page: int = 1
    limit: int = 10


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic model for paginated responses."""
    items: List[T]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_prev: bool
