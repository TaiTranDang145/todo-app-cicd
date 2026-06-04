from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    """
    Schema nhận dữ liệu khi thêm Todo mới.
    """
    pass

class TodoUpdate(BaseModel):
    """
    Schema nhận dữ liệu khi cập nhật Todo. Các trường là tùy chọn (optional).
    """
    title: str | None = None
    completed: bool | None = None

class Todo(TodoBase):
    """
    Schema phản hồi từ API bao gồm cả ID khóa chính.
    """
    id: int

    class Config:
        from_attributes = True
