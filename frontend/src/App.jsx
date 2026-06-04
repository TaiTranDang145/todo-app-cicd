import React, { useState, useEffect } from 'react';
import { getTodos, createTodo, updateTodo, deleteTodo, getHealth } from './api';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [apiStatus, setApiStatus] = useState('checking'); // 'online', 'offline', 'checking'
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'pending', 'completed'

  useEffect(() => {
    fetchBackendData();
    const interval = setInterval(checkHealth, 8000);
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      const data = await getHealth();
      if (data.status === 'ok') {
        setApiStatus('online');
      } else {
        setApiStatus('offline');
      }
    } catch {
      setApiStatus('offline');
    }
  };

  const fetchBackendData = async () => {
    setLoading(true);
    try {
      await checkHealth();
      const data = await getTodos();
      setTodos(data);
    } catch (err) {
      console.error("Lỗi khi tải danh sách todo:", err);
      setApiStatus('offline');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async (e) => {
    e.preventDefault();
    if (!newTodoTitle.trim()) return;

    try {
      const created = await createTodo(newTodoTitle);
      setTodos([...todos, created]);
      setNewTodoTitle('');
    } catch (err) {
      console.error("Không thể thêm todo:", err);
    }
  };

  const handleToggleComplete = async (todo) => {
    try {
      const updated = await updateTodo(todo.id, { completed: !todo.completed });
      setTodos(todos.map(t => t.id === todo.id ? updated : t));
    } catch (err) {
      console.error("Không thể cập nhật todo:", err);
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await deleteTodo(id);
      setTodos(todos.filter(t => t.id !== id));
    } catch (err) {
      console.error("Không thể xóa todo:", err);
    }
  };

  // Lọc danh sách Todo theo tab
  const filteredTodos = todos.filter(todo => {
    if (activeTab === 'pending') return !todo.completed;
    if (activeTab === 'completed') return todo.completed;
    return true;
  });

  return (
    <div className="app-container">
      {/* Background blobs */}
      <div className="glow-orb orb-purple"></div>
      <div className="glow-orb orb-teal"></div>

      <header className="app-header">
        <div className="logo-group">
          <img src="https://img.icons8.com/color/96/todo-list.png" alt="Todo Logo" className="header-logo" />
          <h1>VPI Todo Control Hub</h1>
        </div>
        <p className="app-subtitle">Quản lý công việc hiệu quả trên nền tảng Docker & CI/CD Pipeline tự động</p>
      </header>

      <main className="app-main">
        {/* API Status Alert Banner */}
        <div className={`status-banner ${apiStatus}`}>
          <span className="pulse-dot"></span>
          <span className="status-label">
            {apiStatus === 'online' 
              ? 'KẾT NỐI API BACKEND: ONLINE (FASTAPI + SQLITE)' 
              : apiStatus === 'offline' 
              ? 'LỖI: MẤT KẾT NỐI TỚI API BACKEND' 
              : 'ĐANG KIỂM TRA TRẠNG THÁI KẾT NỐI...'}
          </span>
        </div>

        <div className="todo-container-centered">
          {/* Todo App Card */}
          <section className="card todo-section">
            <h2>Danh Sách Công Việc</h2>
            
            {/* Form thêm Todo mới */}
            <form onSubmit={handleAddTodo} className="todo-form">
              <input
                type="text"
                placeholder="Nhập công việc mới cần làm..."
                value={newTodoTitle}
                onChange={(e) => setNewTodoTitle(e.target.value)}
                disabled={apiStatus === 'offline'}
                className="todo-input"
              />
              <button 
                type="submit" 
                disabled={apiStatus === 'offline' || !newTodoTitle.trim()} 
                className="btn btn-add"
              >
                Thêm Mới
              </button>
            </form>

            {/* Filter Tabs */}
            <div className="filter-tabs">
              <button 
                onClick={() => setActiveTab('all')} 
                className={`tab-btn ${activeTab === 'all' ? 'active' : ''}`}
              >
                Tất cả ({todos.length})
              </button>
              <button 
                onClick={() => setActiveTab('pending')} 
                className={`tab-btn ${activeTab === 'pending' ? 'active' : ''}`}
              >
                Chưa làm ({todos.filter(t => !t.completed).length})
              </button>
              <button 
                onClick={() => setActiveTab('completed')} 
                className={`tab-btn ${activeTab === 'completed' ? 'active' : ''}`}
              >
                Đã xong ({todos.filter(t => t.completed).length})
              </button>
            </div>

            {/* Danh sách items */}
            {loading ? (
              <div className="loading-spinner">Đang tải dữ liệu...</div>
            ) : filteredTodos.length === 0 ? (
              <div className="empty-state">
                <img src="https://img.icons8.com/isometric/100/null-search.png" alt="Empty List" />
                <p>Không có công việc nào trong danh sách!</p>
              </div>
            ) : (
              <div className="todo-list">
                {filteredTodos.map((todo) => (
                  <div key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                    <div 
                      onClick={() => handleToggleComplete(todo)} 
                      className="todo-item-click-area"
                    >
                      <div className="checkbox-outer">
                        {todo.completed && <span className="checkbox-inner">✓</span>}
                      </div>
                      <span className="todo-title-text">{todo.title}</span>
                    </div>
                    <button 
                      onClick={() => handleDeleteTodo(todo.id)} 
                      className="btn-delete"
                      title="Xóa công việc"
                    >
                      &times;
                    </button>
                  </div>
                ))}
              </div>
            )}
          </section>
        </div>
      </main>

      <footer className="app-footer-bar">
        <p>© 2026 DevOps Enterprise Blueprint • Hỗ trợ SQLite & Docker Compose</p>
        <div className="tech-stack-badges">
          <span>React (Vite)</span>
          <span>FastAPI</span>
          <span>SQLite</span>
          <span>Docker</span>
          <span>GitHub Actions</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
