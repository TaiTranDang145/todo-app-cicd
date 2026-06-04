from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Đường dẫn database SQLite lưu trữ cục bộ dưới dạng tệp todo.db
DATABASE_URL = "sqlite:///./todo.db"

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
