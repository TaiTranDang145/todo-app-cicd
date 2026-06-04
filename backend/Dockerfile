# Sử dụng Python image chính thức phiên bản slim nhẹ và bảo mật
FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép file requirements.txt trước để tận dụng cache của Docker layer
COPY requirements.txt .

# Cài đặt các thư viện phụ thuộc
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ source code của backend vào container
COPY . .

# Expose port 8000 của container ra ngoài
EXPOSE 8000

# Lệnh khởi chạy FastAPI app (do main.py nằm trong thư mục app/)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
