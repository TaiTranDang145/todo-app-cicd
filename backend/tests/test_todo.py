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

def test_update_todo():
    """
    Kiểm thử API PUT /todos/{todo_id} (Cập nhật công việc):
    Tạo mới một todo, sau đó gửi request PUT để cập nhật trạng thái completed thành True.
    """
    # 1. Tạo mới todo
    create_resp = client.post(
        "/todos",
        json={"title": "Test Update Task", "completed": False}
    )
    todo_id = create_resp.json()["id"]

    # 2. Gửi request cập nhật
    update_resp = client.put(
        f"/todos/{todo_id}",
        json={"title": "Test Update Task Done", "completed": True}
    )
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["title"] == "Test Update Task Done"
    assert data["completed"] is True

def test_delete_todo():
    """
    Kiểm thử API DELETE /todos/{todo_id} (Xóa công việc):
    Tạo mới một todo, gửi request DELETE để xóa nó, sau đó kiểm tra xem nó còn trong danh sách không.
    """
    # 1. Tạo mới todo
    create_resp = client.post(
        "/todos",
        json={"title": "Test Delete Task", "completed": False}
    )
    todo_id = create_resp.json()["id"]

    # 2. Xóa todo
    delete_resp = client.delete(f"/todos/{todo_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json() == {"message": "Todo deleted successfully"}

    # 3. Kiểm tra xem đã mất trong DB chưa
    get_resp = client.get("/todos")
    titles = [item["title"] for item in get_resp.json()]
    assert "Test Delete Task" not in titles

def test_cors_headers():
    """
    Kiểm thử CORS Headers phản hồi từ API:
    Gửi request OPTIONS (preflight) đến /todos và kiểm tra xem có chứa header Access-Control-Allow-Origin không.
    """
    response = client.options(
        "/todos",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Content-Type",
        }
    )
    assert response.status_code == 200 or response.status_code == 204
    assert response.headers.get("access-control-allow-origin") == "*"

