import sys
import os
import datetime
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


def test_clear_completed():
    """
    Kiểm thử API DELETE /todos/completed (Xóa tất cả các công việc đã hoàn thành):
    1. Tạo 2 công việc (1 hoàn thành, 1 chưa hoàn thành).
    2. Gọi API DELETE /todos/completed.
    3. Kiểm tra xem chỉ công việc hoàn thành bị xóa, công việc chưa hoàn thành vẫn còn.
    """
    # 1. Tạo công việc đã hoàn thành
    client.post(
        "/todos",
        json={"title": "Task Completed A", "completed": True}
    )
    # 2. Tạo công việc chưa hoàn thành
    client.post(
        "/todos",
        json={"title": "Task Pending B", "completed": False}
    )

    # 3. Gọi API clear completed
    response = client.delete("/todos/completed")
    assert response.status_code == 200
    assert "Cleared" in response.json()["message"]

    # 4. Kiểm tra danh sách còn lại
    get_resp = client.get("/todos")
    todos = get_resp.json()
    titles = [item["title"] for item in todos]
    
    # Task Completed A phải biến mất
    assert "Task Completed A" not in titles
    # Task Pending B phải vẫn còn
    assert "Task Pending B" in titles


def test_get_todos_by_date():
    """
    Kiểm thử lọc Todo theo ngày:
    1. Tạo 1 todo cho ngày hôm nay.
    2. Tạo 1 todo cho ngày mai.
    3. Lọc danh sách theo ngày hôm nay -> chỉ chứa todo ngày hôm nay.
    4. Lọc danh sách theo ngày mai -> chỉ chứa todo ngày mai.
    """
    today_str = datetime.date.today().isoformat()
    tomorrow_str = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()

    # Tạo todo hôm nay
    client.post(
        "/todos",
        json={"title": "Task Today", "completed": False, "date": today_str}
    )
    # Tạo todo ngày mai
    client.post(
        "/todos",
        json={"title": "Task Tomorrow", "completed": False, "date": tomorrow_str}
    )

    # Lọc hôm nay
    resp_today = client.get(f"/todos?date={today_str}")
    assert resp_today.status_code == 200
    todos_today = resp_today.json()
    titles_today = [t["title"] for t in todos_today]
    assert "Task Today" in titles_today
    assert "Task Tomorrow" not in titles_today

    # Lọc ngày mai
    resp_tomorrow = client.get(f"/todos?date={tomorrow_str}")
    assert resp_tomorrow.status_code == 200
    todos_tomorrow = resp_tomorrow.json()
    titles_tomorrow = [t["title"] for t in todos_tomorrow]
    assert "Task Tomorrow" in titles_tomorrow
    assert "Task Today" not in titles_tomorrow


def test_get_todos_by_category():
    """
    Kiểm thử lọc Todo theo danh mục (category):
    1. Tạo 1 todo thuộc danh mục "Công việc".
    2. Tạo 1 todo thuộc danh mục "Học tập".
    3. Lọc danh sách theo danh mục "Công việc" -> chỉ chứa todo "Công việc".
    4. Lọc danh sách theo danh mục "Học tập" -> chỉ chứa todo "Học tập".
    """
    # Tạo todo "Công việc"
    client.post(
        "/todos",
        json={"title": "Họp dự án", "completed": False, "category": "Công việc"}
    )
    # Tạo todo "Học tập"
    client.post(
        "/todos",
        json={"title": "Học Docker", "completed": False, "category": "Học tập"}
    )

    # Lọc "Công việc"
    resp_work = client.get("/todos?category=Công việc")
    assert resp_work.status_code == 200
    todos_work = resp_work.json()
    titles_work = [t["title"] for t in todos_work]
    assert "Họp dự án" in titles_work
    assert "Học Docker" not in titles_work

    # Lọc "Học tập"
    resp_study = client.get("/todos?category=Học tập")
    assert resp_study.status_code == 200
    todos_study = resp_study.json()
    titles_study = [t["title"] for t in todos_study]
    assert "Học Docker" in titles_study
    assert "Họp dự án" not in titles_study




