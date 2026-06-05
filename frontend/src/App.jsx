import React, { useState, useEffect } from 'react';
import { getTodos, createTodo, updateTodo, deleteTodo, getHealth, clearCompletedTodos } from './api';

function App() {
  const getIsoDateString = (date) => {
    return date.toISOString().split('T')[0];
  };

  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(today.getDate() - 1);
  const tomorrow = new Date(today);
  tomorrow.setDate(today.getDate() + 1);

  const dateOptions = [
    { label: 'Hôm qua', value: getIsoDateString(yesterday), display: yesterday.toLocaleDateString('vi-VN', { weekday: 'short', day: '2-digit', month: '2-digit' }) },
    { label: 'Hôm nay', value: getIsoDateString(today), display: today.toLocaleDateString('vi-VN', { weekday: 'short', day: '2-digit', month: '2-digit' }) },
    { label: 'Ngày mai', value: getIsoDateString(tomorrow), display: tomorrow.toLocaleDateString('vi-VN', { weekday: 'short', day: '2-digit', month: '2-digit' }) },
  ];

  const [todos, setTodos] = useState([]);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [selectedDate, setSelectedDate] = useState(dateOptions[1].value); // Mặc định là Hôm nay
  const [apiStatus, setApiStatus] = useState('checking'); // 'online', 'offline', 'checking'
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'pending', 'completed'

  useEffect(() => {
    fetchBackendData(selectedDate);
    const interval = setInterval(checkHealth, 8000);
    return () => clearInterval(interval);
  }, [selectedDate]);

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

  const fetchBackendData = async (date) => {
    setLoading(true);
    try {
      await checkHealth();
      const data = await getTodos(date);
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
      const created = await createTodo(newTodoTitle, selectedDate);
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

  const handleClearCompleted = async () => {
    const completedCount = todos.filter(t => t.completed).length;
    if (completedCount === 0) return;
    if (window.confirm(`Bạn có chắc chắn muốn xóa tất cả ${completedCount} công việc đã hoàn thành?`)) {
      try {
        await clearCompletedTodos();
        setTodos(todos.filter(t => !t.completed));
      } catch (err) {
        console.error("Không thể xóa các công việc đã hoàn thành:", err);
      }
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
        <p className="app-subtitle">Quản lý công việc cá nhân</p>
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

            {/* Thanh chọn ngày (Hôm qua, Hôm nay, Ngày mai) */}
            <div className="date-selector" style={{ display: 'flex', justifyContent: 'center', gap: '0.8rem', marginBottom: '1.5rem', background: 'rgba(255, 255, 255, 0.05)', padding: '0.4rem', borderRadius: '12px' }}>
              {dateOptions.map(opt => (
                <button
                  key={opt.value}
                  type="button"
                  onClick={() => setSelectedDate(opt.value)}
                  className={`date-btn ${selectedDate === opt.value ? 'active' : ''}`}
                  style={{
                    flex: 1,
                    padding: '0.6rem 0.8rem',
                    borderRadius: '8px',
                    border: 'none',
                    background: selectedDate === opt.value ? 'linear-gradient(135deg, #a855f7 0%, #14b8a6 100%)' : 'transparent',
                    color: selectedDate === opt.value ? '#ffffff' : 'rgba(255, 255, 255, 0.6)',
                    cursor: 'pointer',
                    fontSize: '0.9rem',
                    fontWeight: selectedDate === opt.value ? '600' : '400',
                    transition: 'all 0.3s ease',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '0.2rem',
                  }}
                >
                  <span style={{ fontSize: '0.75rem', opacity: 0.8, textTransform: 'uppercase' }}>{opt.label}</span>
                  <span>{opt.display}</span>
                </button>
              ))}
            </div>
            
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
                
                {todos.filter(t => t.completed).length > 0 && (
                  <div className="clear-completed-container" style={{ display: 'flex', justifyContent: 'center', marginTop: '1.2rem' }}>
                    <button 
                      onClick={handleClearCompleted} 
                      className="btn btn-clear-completed"
                      style={{
                        background: 'rgba(239, 68, 68, 0.1)',
                        color: '#ef4444',
                        border: '1px solid rgba(239, 68, 68, 0.2)',
                        padding: '0.6rem 1.2rem',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        fontSize: '0.9rem',
                        transition: 'all 0.2s ease',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                        fontWeight: '500',
                      }}
                      onMouseOver={(e) => {
                        e.currentTarget.style.background = 'rgba(239, 68, 68, 0.2)';
                        e.currentTarget.style.transform = 'translateY(-1px)';
                      }}
                      onMouseOut={(e) => {
                        e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)';
                        e.currentTarget.style.transform = 'translateY(0)';
                      }}
                    >
                      🧹 Xóa công việc đã xong ({todos.filter(t => t.completed).length})
                    </button>
                  </div>
                )}
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
