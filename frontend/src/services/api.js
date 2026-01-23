import axios from 'axios';

// Cấu hình Axios để gọi lên Server Django của bạn
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/', 
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
});

// Tự động đính kèm Token nếu user đã đăng nhập
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;