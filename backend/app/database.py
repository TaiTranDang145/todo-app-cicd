from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os
# Xác định thư mục lưu trữ DB tùy thuộc vào môi trường chạy (Docker vs Local)
if os.path.exists("/app") and os.access("/app", os.W_OK):
    DATABASE_DIR = "/app/data"
else:
    # Ở môi trường phát triển local (không chạy Docker)
    DATABASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))

os.makedirs(DATABASE_DIR, exist_ok=True)
DATABASE_URL = f"sqlite:///{DATABASE_DIR}/todo.db"

# Khởi tạo Engine SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Khởi tạo sessionmaker để giao tiếp với DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class cho các ORM models kế thừa
Base = declarative_base()

# Dependency để lấy DB Session cho mỗi request và đóng lại khi hoàn tất
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
