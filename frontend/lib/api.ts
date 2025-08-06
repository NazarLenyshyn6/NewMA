const API_BASE_URL = 'http://localhost:8003';
const CHAT_HISTORY_BASE_URL = 'http://127.0.0.1:8005';

export const apiEndpoints = {
  login: `${API_BASE_URL}/api/v1/gateway/auth/login`,
  register: `${API_BASE_URL}/api/v1/gateway/auth/register`,
  fileUpload: `${API_BASE_URL}/api/v1/gateway/files`,
  sessions: `${API_BASE_URL}/api/v1/gateway/sessions`,
  chat: `${API_BASE_URL}/api/v1/gateway/chat`,
  chatSave: `${API_BASE_URL}/api/v1/gateway/chat/save`,
  chatHistory: `${CHAT_HISTORY_BASE_URL}/api/v1/chat_history`,
};

export const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  const tokenType = localStorage.getItem('token_type') || 'Bearer';
  return {
    'Authorization': `${tokenType} ${token}`,
    'Content-Type': 'application/json',
  };
};

export const apiRequest = async (url: string, options: RequestInit = {}) => {
  const defaultOptions: RequestInit = {
    mode: 'cors',
    credentials: 'include',
    ...options,
  };

  try {
    const response = await fetch(url, defaultOptions);
    return response;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};