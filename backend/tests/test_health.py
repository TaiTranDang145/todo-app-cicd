import sys
import os
# Append thư mục backend vào sys.path để import được module app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    """
    Kiểm thử API GET /health:
    Gửi một request GET tới /health, kiểm tra mã trạng thái trả về là 200 OK 
    và nội dung JSON trả về khớp với định dạng: {"status": "ok"}.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
