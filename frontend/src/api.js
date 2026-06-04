import axios from 'axios';

// Tự động nhận diện IP/Domain của máy chủ để gọi API chính xác
const getApiUrl = () => {
  if (import.meta.env.VITE_API_URL && !import.meta.env.VITE_API_URL.includes('localhost')) {
    return import.meta.env.VITE_API_URL;
  }
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname;
    // Nếu là môi trường chạy local
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'http://localhost:3895';
    }
    // Nếu chạy trên VPS, tự động gọi API tới IP VPS ở cổng 3895
    return `http://${hostname}:3895`;
  }
  return 'http://localhost:3895';
};

const API_URL = getApiUrl();

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getTodos = async () => {
  const response = await api.get('/todos');
  return response.data;
};

export const createTodo = async (title) => {
  const response = await api.post('/todos', { title, completed: false });
  return response.data;
};

export const updateTodo = async (id, updatedFields) => {
  const response = await api.put(`/todos/${id}`, updatedFields);
  return response.data;
};

export const deleteTodo = async (id) => {
  const response = await api.delete(`/todos/${id}`);
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};
