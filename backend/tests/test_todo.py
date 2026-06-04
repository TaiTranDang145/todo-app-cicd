import sys
import os
# Append thư mục backend vào sys.path để import được module app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_todo():
    """
    Kiểm thử API POST /todos (Tạo mới công việc):
    Gửi request POST kèm body JSON chứa tiêu đề và trạng thái.
    Kỳ vọng trả về mã 201 Created và dữ liệu phản hồi chứa ID tự tăng cùng tiêu đề chính xác.
    """
    response = client.post(
        "/todos",
        json={"title": "Học Docker & CI/CD", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Học Docker & CI/CD"
    assert data["completed"] is False
    assert "id" in data

def test_get_todos():
    """
    Kiểm thử API GET /todos (Lấy danh sách công việc):
    Gửi request GET tới /todos.
    Kỳ vọng trả về mã 200 OK và dữ liệu trả về là một danh sách (list).
    Danh sách này phải chứa công việc vừa được tạo trước đó.
    """
    # Tạo trước một công việc mẫu
    client.post(
        "/todos",
        json={"title": "Đọc tài liệu DevOps", "completed": False}
    )
    
    # Lấy danh sách todos
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Kiểm tra xem tiêu đề công việc mẫu có tồn tại trong danh sách hay không
    titles = [item["title"] for item in data]
    assert "Đọc tài liệu DevOps" in titles
