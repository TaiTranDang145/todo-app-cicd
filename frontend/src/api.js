import axios from 'axios';

// Định nghĩa URL gốc của API Backend
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
