import datetime
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models
from sqlalchemy import text
from app import schemas
from app.database import engine, get_db

# Khởi tạo toàn bộ bảng cơ sở dữ liệu nếu chưa tồn tại
models.Base.metadata.create_all(bind=engine)

# Tự động cập nhật thêm cột date nếu cơ sở dữ liệu cũ chưa có (Tránh lỗi trên Production)
try:
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE todos ADD COLUMN date VARCHAR"))
except Exception:
    pass

app = FastAPI(title="Todo Application API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """
    API Health Check để kiểm thử hoạt động của server và CI/CD.
    """
    return {"status": "ok"}

@app.get("/todos", response_model=list[schemas.Todo])
def get_todos(date: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Lấy danh sách các Todo, có thể lọc theo ngày (định dạng YYYY-MM-DD).
    """
    query = db.query(models.Todo)
    if date:
        query = query.filter(models.Todo.date == date)
    return query.all()

@app.post("/todos", response_model=schemas.Todo, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """
    Tạo một Todo mới.
    """
    todo_date = todo.date or datetime.date.today().isoformat()
    db_todo = models.Todo(
        title=todo.title, 
        completed=todo.completed, 
        date=todo_date
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/completed")
def clear_completed_todos(db: Session = Depends(get_db)):
    """
    Xóa tất cả các Todo đã được đánh dấu là hoàn thành (completed=True).
    """
    completed_todos = db.query(models.Todo).filter(models.Todo.completed == True).all()
    count = len(completed_todos)
    db.query(models.Todo).filter(models.Todo.completed == True).delete(synchronize_session=False)
    db.commit()
    return {"message": f"Cleared {count} completed todos successfully"}

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo_update: schemas.TodoUpdate, db: Session = Depends(get_db)):
    """
    Cập nhật thông tin (tiêu đề, trạng thái hoặc ngày) của một Todo.
    """
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_update.title is not None:
        db_todo.title = todo_update.title
    if todo_update.completed is not None:
        db_todo.completed = todo_update.completed
    if todo_update.date is not None:
        db_todo.date = todo_update.date
        
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Xóa một Todo ra khỏi cơ sở dữ liệu.
    """
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
