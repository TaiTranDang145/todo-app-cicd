# --- GIAI ĐOẠN 1: BUILD ---
FROM node:20-alpine AS build

WORKDIR /app

# Copy package configurations
COPY package*.json ./
RUN npm install

# Copy source files
COPY . .

# Định nghĩa các biến build-time cho Vite
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build ứng dụng sang các file tĩnh (dist/)
RUN npm run build

# --- GIAI ĐOẠN 2: PRODUCTION SERVING ---
FROM nginx:stable-alpine

# Copy cấu hình nginx tùy chỉnh chạy ở port 3000
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy kết quả build từ giai đoạn 1 sang thư mục phục vụ web của Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 3000
EXPOSE 3000

# Khởi chạy Nginx
CMD ["nginx", "-g", "daemon off;"]
