from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
    title: str
    completed: bool = False
    date: Optional[str] = None
    category: Optional[str] = "Cá nhân"

class TodoCreate(TodoBase):
    """
    Schema nhận dữ liệu khi thêm Todo mới.
    """
    pass

class TodoUpdate(BaseModel):
    """
    Schema nhận dữ liệu khi cập nhật Todo. Các trường là tùy chọn (optional).
    """
    title: Optional[str] = None
    completed: Optional[bool] = None
    date: Optional[str] = None
    category: Optional[str] = None

class Todo(TodoBase):
    """
    Schema phản hồi từ API bao gồm cả ID khóa chính.
    """
    id: int

    class Config:
        from_attributes = True

