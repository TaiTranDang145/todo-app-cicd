from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Todo(Base):
    """
    ORM Model đại diện cho bảng 'todos' trong SQLite.
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    completed = Column(Boolean, default=False)
