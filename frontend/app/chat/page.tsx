'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Send, Plus, Menu, X, MessageSquare, Brain, Zap, Database, Trash2, User, ChevronDown, Minimize2, Maximize2, MoreVertical, Sparkles, ArrowRight, FileText, Folder, File, Copy, Check } from 'lucide-react';

interface Session {
  id: string;
  title: string;
  created_at: string;
}

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: string;
}

interface FileItem {
  file_name: string;
  storage_uri?: string;
  description?: string;
  summary?: string;
  size?: number;
  type?: string;
  upload_time?: string;
  is_active?: boolean;
}

const ChatPage: React.FC = () => {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSession, setCurrentSession] = useState<Session | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const [showNewSessionModal, setShowNewSessionModal] = useState(false);
  const [newSessionName, setNewSessionName] = useState('');
  const [newSessionError, setNewSessionError] = useState('');
  const [switchingSession, setSwitchingSession] = useState<string | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [sessionToDelete, setSessionToDelete] = useState<Session | null>(null);
  const [deletingSession, setDeletingSession] = useState<string | null>(null);
  const [showSessionOptions, setShowSessionOptions] = useState<string | null>(null);
  const [files, setFiles] = useState<FileItem[]>([]);
  const [showFiles, setShowFiles] = useState(false);
  const [loadingFiles, setLoadingFiles] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileName, setFileName] = useState('');
  const [fileDescription, setFileDescription] = useState('');
  const [uploadError, setUploadError] = useState('');
  const [settingActiveFile, setSettingActiveFile] = useState<string | null>(null);
  const [activeFile, setActiveFile] = useState<FileItem | null>(null);
  const [loadingActiveFile, setLoadingActiveFile] = useState(false);
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Get auth token
  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    const tokenType = localStorage.getItem('token_type') || 'Bearer';
    return {
      'Authorization': `${tokenType} ${token}`,
      'Content-Type': 'application/json',
    };
  };

  // Copy code to clipboard
  const copyToClipboard = async (code: string, codeId: string) => {
    try {
      await navigator.clipboard.writeText(code);
      setCopiedCode(codeId);
      setTimeout(() => setCopiedCode(null), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  // Parse message content to detect code blocks
  const parseMessageContent = (content: string) => {
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = codeBlockRegex.exec(content)) !== null) {
      // Add text before code block
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: content.slice(lastIndex, match.index)
        });
      }

      // Add code block
      parts.push({
        type: 'code',
        language: match[1] || 'text',
        content: match[2].trim()
      });

      lastIndex = match.index + match[0].length;
    }

    // Add remaining text
    if (lastIndex < content.length) {
      parts.push({
        type: 'text',
        content: content.slice(lastIndex)
      });
    }

    return parts.length > 0 ? parts : [{ type: 'text', content }];
  };

  // Render message content with code highlighting
  const renderMessageContent = (content: string, messageId: string, role: 'user' | 'assistant') => {
    const parts = parseMessageContent(content);
    
    return (
      <div className="p-4">
        {parts.map((part, index) => {
          if (part.type === 'code') {
            const codeId = `${messageId}-${index}`;
            return (
              <div key={index} className="my-4 first:mt-0 last:mb-0">
                <div className="bg-gray-900 rounded-t-lg px-4 py-2 flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-gray-400 text-sm font-mono ml-2">{part.language}</span>
                  </div>
                  <button
                    onClick={() => copyToClipboard(part.content, codeId)}
                    className="flex items-center space-x-1 px-2 py-1 text-gray-400 hover:text-white transition-colors rounded text-sm"
                  >
                    {copiedCode === codeId ? (
                      <>
                        <Check className="w-4 h-4" />
                        <span>Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                </div>
                <div className="bg-gray-800 rounded-b-lg p-4 overflow-x-auto">
                  <pre className="text-gray-100 text-sm leading-relaxed font-mono">
                    <code>{part.content}</code>
                  </pre>
                </div>
              </div>
            );
          } else {
            return (
              <div key={index} className="whitespace-pre-wrap leading-relaxed">
                {part.content.trim()}
              </div>
            );
          }
        })}
      </div>
    );
  };

  // Load messages for a session
  const loadMessages = useCallback(async (sessionId: string) => {
    try {
      const response = await fetch(`http://localhost:8003/api/v1/gateway/sessions/${sessionId}/messages`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(data);
      } else {
        console.error('Failed to load messages');
        setMessages([]);
      }
    } catch (error) {
      console.error('Error loading messages:', error);
      setMessages([]);
    }
  }, []);

  // Load sessions from API
  const loadSessions = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:8003/api/v1/gateway/sessions/', {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        const data = await response.json();
        setSessions(data);
      } else {
        console.error('Failed to load sessions');
      }
    } catch (error) {
      console.error('Error loading sessions:', error);
    }
  }, []);

  // Load files from API
  const loadFiles = useCallback(async () => {
    setLoadingFiles(true);
    try {
      const response = await fetch('http://localhost:8003/api/v1/gateway/files/', {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        const data = await response.json();
        setFiles(data);
      } else {
        console.error('Failed to load files');
        setFiles([]);
      }
    } catch (error) {
      console.error('Error loading files:', error);
      setFiles([]);
    } finally {
      setLoadingFiles(false);
    }
  }, []);

  // Get active file for current session
  const getActiveFile = useCallback(async () => {
    if (!currentSession) {
      setActiveFile(null);
      return;
    }

    setLoadingActiveFile(true);
    try {
      const response = await fetch('http://localhost:8003/api/v1/gateway/files/active/', {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        const data = await response.json();
        setActiveFile(data);
      } else {
        console.error('Failed to get active file');
        setActiveFile(null);
      }
    } catch (error) {
      console.error('Error getting active file:', error);
      setActiveFile(null);
    } finally {
      setLoadingActiveFile(false);
    }
  }, [currentSession]);

  // Upload file function
  const uploadFile = async () => {
    if (!selectedFile || !fileName.trim()) {
      setUploadError('Please select a file and provide a name');
      return;
    }

    setUploadingFile(true);
    setUploadProgress(0);
    setUploadError('');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('file_name', fileName.trim());
      formData.append('description', fileDescription.trim());

      const response = await fetch('http://localhost:8003/api/v1/gateway/files/', {
        method: 'POST',
        headers: {
          'Authorization': `${localStorage.getItem('token_type')} ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      });

      if (response.ok) {
        // Refresh files list
        await loadFiles();
        // Close modal and reset form
        setShowUploadModal(false);
        setSelectedFile(null);
        setFileName('');
        setFileDescription('');
        setUploadProgress(100);
      } else {
        const errorData = await response.json().catch(() => ({}));
        setUploadError(errorData.detail || 'Failed to upload file. Please try again.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadError('Network error. Please check your connection and try again.');
    } finally {
      setUploadingFile(false);
      setTimeout(() => setUploadProgress(0), 1000);
    }
  };

  // Set active file for current session
  const setActiveFileForSession = async (fileName: string) => {
    if (!currentSession || settingActiveFile === fileName) return;

    setSettingActiveFile(fileName);
    
    try {
      const response = await fetch('http://localhost:8003/api/v1/gateway/files/active/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          file_name: fileName,
        }),
      });

      if (response.ok) {
        // Refresh files to get updated active status
        await loadFiles();
        // Get the updated active file for display
        await getActiveFile();
      } else {
        console.error('Failed to set active file');
      }
    } catch (error) {
      console.error('Error setting active file:', error);
    } finally {
      setSettingActiveFile(null);
    }
  };

  // Delete file function
  const deleteFile = async (fileName: string) => {
    if (!fileName) {
      console.error('Cannot delete file: no filename provided');
      return;
    }

    console.log('Attempting to delete file:', fileName);
    
    try {
      const response = await fetch(`http://localhost:8003/api/v1/gateway/files/${encodeURIComponent(fileName)}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      console.log('Delete response status:', response.status);
      
      if (response.ok) {
        console.log(`File "${fileName}" deleted successfully`);
        // Refresh files list
        await loadFiles();
      } else {
        const errorText = await response.text();
        console.error('Failed to delete file:', response.status, errorText);
        alert(`Failed to delete file "${fileName}". Error: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting file:', error);
      alert(`Network error while deleting file "${fileName}"`);
    }
  };

  // Initialize sessions
  const initializeSessions = useCallback(async () => {
    await loadSessions();
    
    const isNewLogin = localStorage.getItem('isNewLogin');
    if (isNewLogin === 'true') {
      localStorage.removeItem('isNewLogin');
    }
  }, [loadSessions]);

  // Session persistence - restore active session on load
  const restoreActiveSession = useCallback(async () => {
    const savedSessionId = localStorage.getItem('activeSessionId');
    const savedSessionTitle = localStorage.getItem('activeSessionTitle');
    
    if (savedSessionId && savedSessionTitle && sessions.length > 0) {
      const savedSession = sessions.find(s => s.id === savedSessionId && s.title === savedSessionTitle);
      if (savedSession) {
        setCurrentSession(savedSession);
        loadMessages(savedSession.id);
        // Load files for the restored session
        loadFiles();
        // Get active file for the restored session
        getActiveFile();
      } else {
        // Clean up invalid saved session
        localStorage.removeItem('activeSessionId');
        localStorage.removeItem('activeSessionTitle');
      }
    }
  }, [sessions, loadMessages, loadFiles, getActiveFile]);

  // Check if user is authenticated and initialize
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      window.location.href = '/login';
      return;
    }
    
    initializeSessions();
  }, [initializeSessions]);

  // Restore active session after sessions are loaded
  useEffect(() => {
    if (sessions.length > 0) {
      restoreActiveSession();
    }
  }, [sessions, restoreActiveSession]);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Show new session modal
  const showNewSessionDialog = () => {
    setShowNewSessionModal(true);
    setNewSessionName('');
    setNewSessionError('');
    setShowSessionOptions(null);
  };

  // Create new session with user-provided name
  const createNewSession = async (sessionName: string) => {
    if (!sessionName.trim()) {
      setNewSessionError('Session name is required');
      return;
    }

    setNewSessionError('');

    try {
      const response = await fetch('http://localhost:8003/api/v1/gateway/sessions', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          title: sessionName.trim(),
        }),
      });

      if (response.ok) {
        const newSession = await response.json();
        setSessions(prev => [newSession, ...prev]);
        setCurrentSession(newSession);
        setMessages([]);
        setShowNewSessionModal(false);
        setNewSessionName('');
        
        // Load files for the new session
        loadFiles();
        // Get active file for the new session
        getActiveFile();
        
        // Save new active session to localStorage for persistence
        localStorage.setItem('activeSessionId', newSession.id);
        localStorage.setItem('activeSessionTitle', newSession.title);
        
        try {
          await fetch(`http://localhost:8003/api/v1/gateway/sessions/active/${newSession.title}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({
              title: newSession.title,
            }),
          });
        } catch (error) {
          console.error('Failed to set new session as active:', error);
        }
      } else if (response.status === 409) {
        setNewSessionError('A chat with this name already exists. Please choose a different name.');
      } else {
        console.error('Failed to create session');
        setNewSessionError('Failed to create session. Please try again.');
      }
    } catch (error) {
      console.error('Error creating session:', error);
      setNewSessionError('Network error. Please check your connection and try again.');
    }
  };

  // Handle new session form submission
  const handleNewSessionSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createNewSession(newSessionName);
  };

  // Show modal for new session
  const createQuickNewSession = () => {
    showNewSessionDialog();
  };

  // Show delete confirmation
  const showDeleteConfirmation = (session: Session) => {
    if (currentSession?.id === session.id) {
      console.warn('Cannot delete active session');
      return;
    }
    
    setSessionToDelete(session);
    setShowDeleteConfirm(true);
    setShowSessionOptions(null);
  };

  // Delete session function
  const deleteSession = async () => {
    if (!sessionToDelete || deletingSession) return;

    setDeletingSession(sessionToDelete.id);
    
    try {
      const response = await fetch(`http://localhost:8003/api/v1/gateway/sessions/${sessionToDelete.title}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        setSessions(prev => prev.filter(s => s.id !== sessionToDelete.id));
        console.log(`Session "${sessionToDelete.title}" deleted successfully`);
        
        // Clear session persistence data if the deleted session was saved as active
        const savedSessionId = localStorage.getItem('activeSessionId');
        if (savedSessionId === sessionToDelete.id) {
          localStorage.removeItem('activeSessionId');
          localStorage.removeItem('activeSessionTitle');
        }
      } else {
        console.error('Failed to delete session');
      }
    } catch (error) {
      console.error('Error deleting session:', error);
    } finally {
      setDeletingSession(null);
      setShowDeleteConfirm(false);
      setSessionToDelete(null);
    }
  };

  // Send message
  const sendMessage = async () => {
    if (!inputMessage.trim() || !currentSession || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      role: 'user',
      timestamp: new Date().toISOString(),
    };

    const currentQuestion = inputMessage;
    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(`http://localhost:8003/api/v1/gateway/chat/?question=${encodeURIComponent(currentQuestion)}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        // Check if response is JSON or plain text
        const contentType = response.headers.get('content-type');
        let content;
        
        if (contentType && contentType.includes('application/json')) {
          const data = await response.json();
          content = data.response || data.message || data.answer || JSON.stringify(data);
        } else {
          // Handle plain text response
          content = await response.text();
        }
        
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: content || 'No response received',
          role: 'assistant',
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: 'Sorry, I encountered an error. Please try again.',
          role: 'assistant',
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        role: 'assistant',
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('token_type');
    // Clear session persistence data on explicit logout
    localStorage.removeItem('activeSessionId');
    localStorage.removeItem('activeSessionTitle');
    window.location.href = '/login';
  };

  // Switch session
  const switchSession = async (session: Session) => {
    if (switchingSession === session.id || currentSession?.id === session.id) {
      return;
    }

    setSwitchingSession(session.id);
    setShowSessionOptions(null);
    
    try {
      const response = await fetch(`http://localhost:8003/api/v1/gateway/sessions/active/${session.title}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          title: session.title,
        }),
      });

      if (response.ok) {
        setCurrentSession(session);
        loadMessages(session.id);
        // Load files for the new session
        loadFiles();
        // Get active file for the new session
        getActiveFile();
        // Save active session to localStorage for persistence
        localStorage.setItem('activeSessionId', session.id);
        localStorage.setItem('activeSessionTitle', session.title);
      } else {
        console.error('Failed to set active session on backend');
        setCurrentSession(session);
        loadMessages(session.id);
        // Load files for the new session
        loadFiles();
        // Get active file for the new session
        getActiveFile();
        // Save active session even if backend call fails
        localStorage.setItem('activeSessionId', session.id);
        localStorage.setItem('activeSessionTitle', session.title);
      }
    } catch (error) {
      console.error('Error switching session:', error);
      setCurrentSession(session);
      loadMessages(session.id);
      // Load files for the new session
      loadFiles();
      // Get active file for the new session
      getActiveFile();
      // Save active session even if there's an error
      localStorage.setItem('activeSessionId', session.id);
      localStorage.setItem('activeSessionTitle', session.title);
    } finally {
      setSwitchingSession(null);
    }
  };

  // Close session options when clicking outside
  useEffect(() => {
    const handleClickOutside = () => {
      setShowSessionOptions(null);
    };
    
    if (showSessionOptions) {
      document.addEventListener('click', handleClickOutside);
      return () => document.removeEventListener('click', handleClickOutside);
    }
  }, [showSessionOptions]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-green-100">
      <div className="h-screen flex">
        {/* Modern Sidebar */}
        <div className={`${
          sidebarOpen ? (sidebarCollapsed ? 'w-16' : 'w-80') : 'w-0'
        } transition-all duration-500 ease-in-out overflow-hidden`}>
          <div className="h-full bg-white/80 backdrop-blur-xl border-r border-white/50 shadow-2xl rounded-r-3xl flex flex-col">
            {/* Sidebar Header */}
            <div className="p-6 border-b border-gray-200/50">
              <div className="flex items-center justify-between">
                {!sidebarCollapsed && (
                  <div className="flex items-center space-x-3 opacity-0 animate-fade-in" style={{ animationDelay: '0.2s' }}>
                    <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg">
                      <Brain className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h1 className="text-lg font-bold text-gray-800">ML Agent</h1>
                      <p className="text-xs text-gray-500">Intelligent Assistant</p>
                    </div>
                  </div>
                )}
                
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
                    className="p-2 hover:bg-gray-100 rounded-xl transition-all duration-300 group"
                    title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
                  >
                    {sidebarCollapsed ? 
                      <Maximize2 className="w-4 h-4 text-gray-600 group-hover:text-gray-800" /> :
                      <Minimize2 className="w-4 h-4 text-gray-600 group-hover:text-gray-800" />
                    }
                  </button>
                  
                  <button
                    onClick={() => setSidebarOpen(false)}
                    className="lg:hidden p-2 hover:bg-gray-100 rounded-xl transition-all duration-300"
                  >
                    <X className="w-4 h-4 text-gray-600" />
                  </button>
                </div>
              </div>

              {/* New Chat Button */}
              {!sidebarCollapsed && (
                <button
                  onClick={createQuickNewSession}
                  className="w-full mt-4 flex items-center justify-center space-x-3 px-4 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl opacity-0 animate-fade-in"
                  style={{ animationDelay: '0.4s' }}
                >
                  <Plus className="w-5 h-5" />
                  <span className="font-medium">New Chat</span>
                  <Sparkles className="w-4 h-4" />
                </button>
              )}

              {sidebarCollapsed && (
                <button
                  onClick={createQuickNewSession}
                  className="w-full mt-4 flex items-center justify-center p-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
                  title="New Chat"
                >
                  <Plus className="w-5 h-5" />
                </button>
              )}
            </div>

            {/* Chat Sessions - Tab Style */}
            {sessions.length > 0 && (
              <div className="flex-1 p-4 overflow-hidden">
                {!sidebarCollapsed && (
                  <h3 className="text-sm font-semibold text-gray-700 mb-4 opacity-0 animate-fade-in" style={{ animationDelay: '0.6s' }}>
                    Recent Conversations
                  </h3>
                )}
                
                <div className="space-y-2 max-h-full overflow-y-auto custom-scrollbar" style={{ position: 'relative' }}>
                  {sessions.map((session, index) => (
                    <div
                      key={session.id}
                      className={`group relative rounded-2xl transition-all duration-300 transform hover:scale-102 opacity-0 animate-slide-in`}
                      style={{ animationDelay: `${0.1 * index + 0.8}s` }}
                    >
                      {/* Tab-style session */}
                      <div
                        className={`relative overflow-hidden rounded-2xl transition-all duration-300 ${
                          currentSession?.id === session.id
                            ? 'bg-gradient-to-r from-purple-500 to-blue-600 text-white shadow-lg transform scale-105'
                            : 'bg-white/70 hover:bg-white/90 text-gray-700 shadow-md hover:shadow-lg'
                        } ${switchingSession === session.id ? 'opacity-70' : ''}`}
                      >
                        <button
                          onClick={() => switchSession(session)}
                          disabled={switchingSession === session.id}
                          className="w-full text-left p-4 pr-12 transition-all duration-300"
                        >
                          {!sidebarCollapsed ? (
                            <div className="flex items-center space-x-3">
                              <div className={`w-3 h-3 rounded-full transition-all duration-300 ${
                                currentSession?.id === session.id ? 'bg-white/80' : 'bg-gray-400'
                              }`} />
                              <div className="flex-1 min-w-0">
                                <div className={`font-semibold truncate text-sm transition-all duration-300 ${
                                  currentSession?.id === session.id ? 'text-white' : 'text-gray-800'
                                }`}>
                                  {session.title}
                                </div>
                                <div className={`text-xs truncate transition-all duration-300 ${
                                  currentSession?.id === session.id ? 'text-white/70' : 'text-gray-500'
                                }`}>
                                  {new Date(session.created_at).toLocaleDateString()}
                                </div>
                              </div>
                            </div>
                          ) : (
                            <div className="flex items-center justify-center">
                              <MessageSquare className={`w-4 h-4 ${
                                currentSession?.id === session.id ? 'text-white' : 'text-gray-600'
                              }`} />
                            </div>
                          )}
                        </button>
                        
                        {/* Direct Delete Button */}
                        {!sidebarCollapsed && currentSession?.id !== session.id && (
                          <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                showDeleteConfirmation(session);
                              }}
                              className="p-1 opacity-60 group-hover:opacity-100 hover:bg-red-50 rounded-lg transition-all duration-300"
                              disabled={deletingSession === session.id}
                              title="Delete session"
                            >
                              {deletingSession === session.id ? (
                                <div className="w-4 h-4 border border-red-400 border-t-transparent rounded-full animate-spin" />
                              ) : (
                                <Trash2 className="w-4 h-4 text-red-500 hover:text-red-700" />
                              )}
                            </button>
                          </div>
                        )}
                        
                        {/* Active Session Indicator */}
                        {currentSession?.id === session.id && (
                          <div className="absolute left-0 top-0 bottom-0 w-1 bg-white rounded-r-full" />
                        )}
                        
                        {/* Switching Indicator */}
                        {switchingSession === session.id && (
                          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* User Profile */}
            <div className="p-4 border-t border-gray-200/50">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-gray-600 to-gray-800 rounded-2xl flex items-center justify-center shadow-lg">
                  <User className="w-5 h-5 text-white" />
                </div>
                {!sidebarCollapsed && (
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-gray-800 truncate">User</div>
                    <button
                      onClick={handleLogout}
                      className="text-xs text-gray-500 hover:text-red-600 transition-colors"
                    >
                      Sign out
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <div className="bg-white/80 backdrop-blur-xl border-b border-white/50 px-6 py-4 shadow-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                {!sidebarOpen && (
                  <button
                    onClick={() => setSidebarOpen(true)}
                    className="p-2 hover:bg-gray-100 rounded-xl transition-all duration-300"
                  >
                    <Menu className="w-5 h-5 text-gray-600" />
                  </button>
                )}
                
                <div>
                  <div className="flex items-center space-x-3">
                    <h1 className="text-xl font-bold text-gray-800">
                      {currentSession?.title || 'Welcome to ML Agent'}
                    </h1>
                    {activeFile && activeFile.file_name && (
                      <div className="flex items-center space-x-2 px-3 py-1 bg-green-50 border border-green-200 rounded-xl">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                        <span className="text-sm text-green-700 font-medium">
                          {activeFile.file_name}
                        </span>
                      </div>
                    )}
                    {loadingActiveFile && (
                      <div className="flex items-center space-x-2 px-3 py-1 bg-gray-50 border border-gray-200 rounded-xl">
                        <div className="w-3 h-3 border border-gray-400 border-t-transparent rounded-full animate-spin"></div>
                        <span className="text-sm text-gray-500">
                          Loading...
                        </span>
                      </div>
                    )}
                  </div>
                  {currentSession && (
                    <p className="text-sm text-gray-500 mt-1">
                      Created {new Date(currentSession.created_at).toLocaleDateString()}
                    </p>
                  )}
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                {/* Files Button */}
                {currentSession && (
                  <button
                    onClick={() => {
                      setShowFiles(!showFiles);
                      if (!showFiles && files.length === 0) {
                        loadFiles();
                      }
                    }}
                    className="flex items-center space-x-2 px-4 py-2 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-xl transition-all duration-300"
                    title="View uploaded files"
                  >
                    <Folder className="w-4 h-4 text-gray-600" />
                    <span className="text-sm font-medium text-gray-800">Files</span>
                    {files.length > 0 && (
                      <span className="bg-gray-800 text-white text-xs rounded-full px-2 py-0.5 ml-1">
                        {files.length}
                      </span>
                    )}
                  </button>
                )}
                
                <div className="flex items-center space-x-2 bg-gradient-to-r from-purple-100 to-blue-100 rounded-2xl px-4 py-2">
                  <User className="w-4 h-4 text-gray-600" />
                  <span className="text-sm font-medium text-gray-700">User</span>
                  <ChevronDown className="w-4 h-4 text-gray-600" />
                </div>
              </div>
            </div>
          </div>

          {!currentSession ? (
            // Enhanced Welcome Screen
            <div className="flex-1 flex flex-col justify-center px-8 py-12">
              <div className="max-w-4xl mx-auto text-center">
                <div className="mb-8 opacity-0 animate-fade-in" style={{ animationDelay: '0.2s' }}>
                  <div className="w-24 h-24 bg-gradient-to-br from-purple-500 to-blue-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-2xl">
                    <Brain className="w-12 h-12 text-white" />
                  </div>
                  <h1 className="text-5xl font-bold text-gray-800 mb-4">
                    Hi there, <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">User</span>
                  </h1>
                  <h2 className="text-3xl text-gray-600 mb-12">
                    What would you like to <span className="text-orange-500 font-bold">discover?</span>
                  </h2>
                </div>

                {/* Enhanced Quick Action Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                  <div className="bg-white/70 backdrop-blur-sm rounded-3xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-500 cursor-pointer transform hover:scale-105 opacity-0 animate-slide-in" style={{ animationDelay: '0.4s' }}>
                    <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl flex items-center justify-center mb-6 shadow-lg">
                      <Database className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-gray-800 mb-3">
                      Revenue Analysis by Demographics
                    </h3>
                    <p className="text-gray-600 text-sm leading-relaxed mb-4">
                      How does the distribution of revenue total vary based on the gender of customers?
                    </p>
                    <div className="flex items-center text-purple-600 font-medium">
                      <span className="text-sm">Explore now</span>
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </div>
                  </div>

                  <div className="bg-white/70 backdrop-blur-sm rounded-3xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-500 cursor-pointer transform hover:scale-105 opacity-0 animate-slide-in" style={{ animationDelay: '0.6s' }}>
                    <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-blue-500 rounded-2xl flex items-center justify-center mb-6 shadow-lg">
                      <Zap className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-gray-800 mb-3">
                      Customer Behavior Insights  
                    </h3>
                    <p className="text-gray-600 text-sm leading-relaxed mb-4">
                      What is the average time spent on the website for customers who made purchases using Credit Cards?
                    </p>
                    <div className="flex items-center text-purple-600 font-medium">
                      <span className="text-sm">Analyze now</span>
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </div>
                  </div>
                </div>

                {/* Enhanced CTA */}
                <div className="opacity-0 animate-fade-in" style={{ animationDelay: '0.8s' }}>
                  <button
                    onClick={showNewSessionDialog}
                    className="inline-flex items-center space-x-3 px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-2xl font-bold text-lg transition-all duration-300 transform hover:scale-105 shadow-2xl hover:shadow-3xl"
                  >
                    <Plus className="w-5 h-5" />
                    <span>Start New Conversation</span>
                    <Sparkles className="w-5 h-5" />
                  </button>

                  {sessions.length > 0 && (
                    <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl border border-blue-200/50">
                      <p className="text-blue-800 font-medium">
                        💡 <strong>Tip:</strong> You have {sessions.length} previous conversation{sessions.length !== 1 ? 's' : ''}. 
                        Select one from the sidebar to continue where you left off.
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            // Enhanced Chat Interface
            <>
              {/* Messages Area */}
              <div className="flex-1 overflow-y-auto p-6 bg-gray-50/30 custom-scrollbar">
                {messages.length === 0 ? (
                  <div className="text-center text-gray-400 mt-20 opacity-0 animate-fade-in">
                    <div className="w-20 h-20 bg-gradient-to-br from-purple-100 to-blue-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
                      <Brain className="w-10 h-10 text-purple-500" />
                    </div>
                    <h3 className="text-2xl font-bold mb-4 text-gray-700">Ready to assist you</h3>
                    <p className="text-lg">Ask me anything about your data or ML tasks!</p>
                  </div>
                ) : (
                  messages.map((message, index) => (
                    <div
                      key={message.id}
                      className={`w-full flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-6 opacity-0 animate-slide-in`}
                      style={{ animationDelay: `${index * 0.1}s` }}
                    >
                      <div className={`flex items-start space-x-4 max-w-4xl ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                        {/* Avatar */}
                        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg ${
                          message.role === 'user'
                            ? 'bg-gradient-to-r from-purple-600 to-blue-600'
                            : 'bg-gradient-to-r from-green-600 to-emerald-600'
                        }`}>
                          {message.role === 'user' ? (
                            <User className="w-5 h-5 text-white" />
                          ) : (
                            <Brain className="w-5 h-5 text-white" />
                          )}
                        </div>
                        
                        {/* Message Content */}
                        <div className={`flex-1 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                          <div className={`inline-block rounded-2xl shadow-lg transition-all duration-300 ${
                            message.role === 'user'
                              ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-br-md'
                              : 'bg-white border border-gray-200 text-gray-800 rounded-bl-md overflow-hidden'
                          }`}>
                            <div className="text-sm">
                              {renderMessageContent(message.content, message.id, message.role)}
                            </div>
                          </div>
                          <div className={`text-xs text-gray-500 mt-2 px-2 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                            <span>{new Date(message.timestamp).toLocaleTimeString()}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                )}
                
                {isLoading && (
                  <div className="w-full flex justify-start mb-6 opacity-0 animate-fade-in">
                    <div className="flex items-start space-x-4 max-w-4xl">
                      {/* AI Avatar */}
                      <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg bg-gradient-to-r from-green-600 to-emerald-600">
                        <Brain className="w-5 h-5 text-white animate-pulse" />
                      </div>
                      
                      {/* Loading Message */}
                      <div className="flex-1">
                        <div className="inline-block p-4 rounded-2xl rounded-bl-md shadow-lg bg-white border border-gray-200">
                          <div className="flex items-center space-x-3">
                            {/* Advanced Loading Animation */}
                            <div className="flex items-center space-x-1">
                              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                            </div>
                            <div className="flex flex-col space-y-1">
                              <div className="flex items-center space-x-2">
                                <span className="text-sm text-gray-600 font-medium">AI is analyzing your data</span>
                                <div className="flex space-x-1">
                                  <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce"></div>
                                  <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                                  <div className="w-1 h-1 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                </div>
                              </div>
                              {/* Progress indicators */}
                              <div className="flex items-center space-x-2 text-xs text-gray-500">
                                <Zap className="w-3 h-3 text-yellow-500 animate-pulse" />
                                <span>Processing patterns and insights...</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* ChatGPT-style Input Area */}
              <div className="p-6 bg-white">
                <div className="max-w-4xl mx-auto">
                  <div className="relative flex items-end space-x-4">
                    <div className="flex-1">
                      <div className="relative">
                        <textarea
                          value={inputMessage}
                          onChange={(e) => setInputMessage(e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                              e.preventDefault();
                              sendMessage();
                            }
                          }}
                          placeholder={`Message ML Agent${activeFile?.file_name ? ` about ${activeFile.file_name}` : ''}...`}
                          className="w-full p-4 pr-12 rounded-2xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-gray-900 placeholder-gray-500 bg-white resize-none transition-all duration-200 shadow-sm hover:shadow-md min-h-[56px] max-h-32 overflow-y-auto"
                          disabled={isLoading}
                          rows={1}
                          style={{
                            height: 'auto',
                            minHeight: '56px',
                            maxHeight: '128px'
                          }}
                          onInput={(e) => {
                            const target = e.target as HTMLTextAreaElement;
                            target.style.height = 'auto';
                            target.style.height = Math.min(target.scrollHeight, 128) + 'px';
                          }}
                        />
                        <button
                          onClick={sendMessage}
                          disabled={!inputMessage.trim() || isLoading}
                          className="absolute right-2 bottom-2 p-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed rounded-xl transition-all duration-200 shadow-sm hover:shadow-md"
                        >
                          <Send className="w-4 h-4 text-white" />
                        </button>
                      </div>
                    </div>
                  </div>
                  
                  {/* Helper text */}
                  <div className="mt-3 flex items-center justify-center space-x-4 text-xs text-gray-500">
                    <div className="flex items-center space-x-1">
                      <Database className="w-3 h-3" />
                      <span>{currentSession?.title}</span>
                    </div>
                    {activeFile?.file_name && (
                      <div className="flex items-center space-x-1">
                        <File className="w-3 h-3 text-green-600" />
                        <span className="text-green-600">{activeFile.file_name}</span>
                      </div>
                    )}
                    <span>•</span>
                    <span>Press Enter to send, Shift+Enter for new line</span>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Files Panel */}
        {showFiles && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 flex justify-end">
            <div className="w-full max-w-md bg-white/95 backdrop-blur-xl shadow-2xl border-l border-white/50 opacity-0 animate-slide-in">
              {/* Files Header */}
              <div className="p-6 border-b border-gray-200/50">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gray-800 rounded-xl flex items-center justify-center shadow-lg">
                      <Folder className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h2 className="text-xl font-bold text-gray-800">Your Files</h2>
                      <p className="text-sm text-gray-600">
                        {files.length} file{files.length !== 1 ? 's' : ''} available
                        {activeFile && activeFile.file_name && (
                          <span className="ml-2 text-green-600 font-medium">
                            • {activeFile.file_name} active in "{currentSession?.title}"
                          </span>
                        )}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => {
                        setShowUploadModal(true);
                        setShowFiles(false);
                      }}
                      className="p-2 bg-gray-800 hover:bg-gray-900 text-white rounded-xl transition-colors"
                      title="Upload new file"
                    >
                      <Plus className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => setShowFiles(false)}
                      className="p-2 hover:bg-gray-100 rounded-xl transition-all duration-300"
                    >
                      <X className="w-5 h-5 text-gray-600" />
                    </button>
                  </div>
                </div>
              </div>

              {/* Files Content */}
              <div className="flex-1 p-6 overflow-y-auto max-h-[calc(100vh-120px)]">
                {loadingFiles ? (
                  <div className="flex items-center justify-center py-12">
                    <div className="flex flex-col items-center space-y-4">
                      <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                      <p className="text-gray-600">Loading files...</p>
                    </div>
                  </div>
                ) : files.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-12 text-center">
                    <div className="w-16 h-16 bg-gray-100 rounded-3xl flex items-center justify-center mb-4">
                      <FileText className="w-8 h-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-semibold text-gray-800 mb-2">No files uploaded</h3>
                    <p className="text-gray-500 text-sm">
                      Upload files to your session to see them here
                    </p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {files.map((file, index) => (
                      <div
                        key={file.file_name || index}
                        className={`relative rounded-xl border shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer ${
                          activeFile && activeFile.file_name === file.file_name
                            ? 'bg-green-50 border-green-200 transform scale-102'
                            : 'bg-gray-50 border-gray-200 hover:bg-white'
                        } ${settingActiveFile === file.file_name ? 'opacity-70' : ''}`}
                        onClick={() => currentSession && setActiveFileForSession(file.file_name || '')}
                      >
                        <div className="flex items-center space-x-4 p-4">
                          <div className={`w-10 h-10 rounded-xl flex items-center justify-center shadow-md ${
                            activeFile && activeFile.file_name === file.file_name ? 'bg-green-600' : 'bg-gray-800'
                          }`}>
                          <File className="w-5 h-5 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className="font-semibold text-gray-800 truncate">
                            {file.file_name || 'Unnamed File'}
                          </div>
                          {file.description && (
                            <div className="text-xs text-gray-600 truncate">
                              {file.description}
                            </div>
                          )}
                          {file.size && (
                            <div className="text-xs text-gray-600">
                              {(file.size / 1024 / 1024).toFixed(2)} MB
                            </div>
                          )}
                          {file.upload_time && (
                            <div className="text-xs text-gray-600">
                              {new Date(file.upload_time).toLocaleDateString()}
                            </div>
                          )}
                          </div>
                        </div>
                        
                        {/* Active Indicator */}
                        {activeFile && activeFile.file_name === file.file_name && (
                          <div className="absolute left-0 top-0 bottom-0 w-1 bg-green-600 rounded-r-full" />
                        )}
                        
                        {/* Setting Active Indicator */}
                        {settingActiveFile === file.file_name && (
                          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin text-green-600" />
                          </div>
                        )}
                        
                        {/* Delete Button */}
                        <div className="absolute right-2 top-2">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              console.log('Deleting file:', file.file_name);
                              deleteFile(file.file_name || '');
                            }}
                            className="p-1 opacity-60 hover:opacity-100 hover:bg-red-50 text-red-500 hover:text-red-700 rounded-lg transition-all duration-300"
                            title={`Delete ${file.file_name}`}
                          >
                            <Trash2 className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Files Footer */}
              <div className="p-6 border-t border-gray-200/50 bg-gradient-to-r from-blue-50 to-purple-50">
                <div className="flex items-center space-x-2 text-sm text-blue-800">
                  <FileText className="w-4 h-4" />
                  <span className="font-medium">
                    💡 Tip: These files are available for analysis in your current session
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Upload File Modal */}
        {showUploadModal && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-white/95 backdrop-blur-xl rounded-3xl p-8 w-full max-w-lg shadow-2xl border border-white/50 opacity-0 animate-modal-in">
              <div className="text-center mb-8">
                <div className="w-16 h-16 bg-gray-800 rounded-3xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                  <Plus className="w-8 h-8 text-white" />
                </div>
                <h2 className="text-3xl font-bold text-gray-800 mb-2">Upload File</h2>
                <p className="text-gray-600">Add a new file to your data collection</p>
              </div>

              {/* Upload Form */}
              <div className="space-y-6">
                {/* File Selection */}
                <div>
                  <label className="block text-sm font-semibold mb-3 text-gray-700">
                    Select File
                  </label>
                  {!selectedFile ? (
                    <div 
                      onClick={() => fileInputRef.current?.click()}
                      className="w-full p-8 border-2 border-dashed border-gray-300 rounded-2xl text-center cursor-pointer hover:border-blue-400 hover:bg-blue-50/50 transition-all duration-300"
                    >
                      <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                      <p className="text-gray-600 font-medium">Click to select a file</p>
                      <p className="text-sm text-gray-500 mt-2">Supported formats: CSV, JSON, TXT, etc.</p>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-4 p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-2xl border border-green-200">
                      <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-blue-600 rounded-xl flex items-center justify-center shadow-md">
                        <File className="w-5 h-5 text-white" />
                      </div>
                      <div className="flex-1">
                        <div className="font-semibold text-gray-800">{selectedFile.name}</div>
                        <div className="text-sm text-gray-500">
                          {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                        </div>
                      </div>
                      <button
                        onClick={() => {
                          setSelectedFile(null);
                          setFileName('');
                        }}
                        className="p-2 hover:bg-red-100 text-red-500 rounded-lg transition-all duration-300"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  )}
                  <input
                    ref={fileInputRef}
                    type="file"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) {
                        setSelectedFile(file);
                        setFileName(file.name.split('.')[0]);
                      }
                    }}
                    className="hidden"
                    accept=".csv,.json,.txt,.xlsx,.xls"
                  />
                </div>

                {/* File Name */}
                <div>
                  <label className="block text-sm font-semibold mb-3 text-gray-700">
                    File Name
                  </label>
                  <input
                    type="text"
                    value={fileName}
                    onChange={(e) => {
                      setFileName(e.target.value);
                      if (uploadError) setUploadError('');
                    }}
                    placeholder="Enter a name for your file..."
                    className={`w-full px-4 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-gray-800 focus:border-transparent transition-all ${
                      uploadError ? 'border-red-300 focus:ring-red-500' : ''
                    }`}
                  />
                </div>

                {/* Description (Optional) */}
                <div>
                  <label className="block text-sm font-semibold mb-3 text-gray-700">
                    Description <span className="text-gray-400 font-normal">(Optional)</span>
                  </label>
                  <textarea
                    value={fileDescription}
                    onChange={(e) => setFileDescription(e.target.value)}
                    placeholder="Describe what this file contains..."
                    rows={3}
                    className="w-full px-4 py-4 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-gray-800 focus:border-transparent transition-all resize-none"
                  />
                </div>

                {/* Upload Progress */}
                {uploadingFile && (
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Uploading...</span>
                      <span className="text-blue-600 font-medium">{uploadProgress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-gray-800 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                {/* Error Message */}
                {uploadError && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-2xl">
                    <p className="text-sm text-red-600">{uploadError}</p>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex space-x-4 pt-4">
                  <button
                    type="button"
                    onClick={() => {
                      setShowUploadModal(false);
                      setSelectedFile(null);
                      setFileName('');
                      setFileDescription('');
                      setUploadError('');
                    }}
                    disabled={uploadingFile}
                    className="flex-1 px-4 py-4 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 hover:bg-gray-100 transition-colors font-semibold disabled:opacity-50"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={uploadFile}
                    disabled={!selectedFile || !fileName.trim() || uploadingFile}
                    className="flex-1 px-4 py-4 bg-gray-800 text-white hover:bg-gray-900 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-semibold rounded-xl flex items-center justify-center space-x-2"
                  >
                    {uploadingFile ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Uploading...</span>
                      </>
                    ) : (
                      <>
                        <Plus className="w-4 h-4" />
                        <span>Upload File</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Enhanced New Session Modal */}
      {showNewSessionModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white/95 backdrop-blur-xl rounded-3xl p-8 w-full max-w-lg shadow-2xl border border-white/50 opacity-0 animate-modal-in">
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-blue-600 rounded-3xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                <Plus className="w-8 h-8 text-white" />
              </div>
              <h2 className="text-3xl font-bold text-gray-800 mb-2">Create New Chat</h2>
              <p className="text-gray-600">Start a new conversation with your AI assistant</p>
            </div>
            
            <form onSubmit={handleNewSessionSubmit} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold mb-3 text-gray-700">
                  Chat Name
                </label>
                <input
                  type="text"
                  value={newSessionName}
                  onChange={(e) => {
                    setNewSessionName(e.target.value);
                    if (newSessionError) setNewSessionError('');
                  }}
                  placeholder="Enter a descriptive name for your chat..."
                  className={`w-full p-4 rounded-2xl border-2 ${
                    newSessionError ? 'border-red-300 focus:ring-red-500/20' : 'border-gray-200 focus:ring-purple-500/20'
                  } focus:outline-none focus:ring-4 text-gray-800 placeholder-gray-500 bg-white/70 transition-all duration-300`}
                  autoFocus
                />
                {newSessionError && (
                  <p className="mt-3 text-sm text-red-600 bg-red-50 p-3 rounded-xl">{newSessionError}</p>
                )}
              </div>
              
              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => {
                    setShowNewSessionModal(false);
                    setNewSessionError('');
                  }}
                  className="flex-1 p-4 rounded-2xl border-2 border-gray-200 text-gray-700 hover:bg-gray-50 transition-all duration-300 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!newSessionName.trim()}
                  className="flex-1 p-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 text-white rounded-2xl disabled:cursor-not-allowed transition-all duration-300 font-semibold shadow-lg hover:shadow-xl transform hover:scale-105"
                >
                  Create Chat
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Enhanced Delete Confirmation Modal */}
      {showDeleteConfirm && sessionToDelete && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white/95 backdrop-blur-xl rounded-3xl p-8 w-full max-w-md shadow-2xl border border-white/50 opacity-0 animate-modal-in">
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-red-100 rounded-3xl flex items-center justify-center mx-auto mb-4">
                <Trash2 className="w-8 h-8 text-red-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Delete Chat</h2>
              <p className="text-gray-600">This action cannot be undone</p>
            </div>
            
            <div className="mb-8 p-6 bg-gradient-to-r from-red-50 to-pink-50 rounded-2xl border border-red-200/50">
              <p className="text-gray-700 text-center">
                Are you sure you want to delete <strong>&quot;{sessionToDelete.title}&quot;</strong>?
              </p>
              <p className="text-sm text-gray-500 text-center mt-2">
                All messages in this chat will be permanently removed.
              </p>
            </div>

            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => {
                  setShowDeleteConfirm(false);
                  setSessionToDelete(null);
                }}
                disabled={deletingSession === sessionToDelete.id}
                className="flex-1 p-4 rounded-2xl border-2 border-gray-200 text-gray-700 hover:bg-gray-50 transition-all duration-300 font-semibold disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={deleteSession}
                disabled={deletingSession === sessionToDelete.id}
                className="flex-1 p-4 bg-red-600 text-white rounded-2xl hover:bg-red-700 disabled:bg-red-400 disabled:cursor-not-allowed transition-all duration-300 font-semibold flex items-center justify-center shadow-lg hover:shadow-xl"
              >
                {deletingSession === sessionToDelete.id ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Deleting...
                  </>
                ) : (
                  'Delete Chat'
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #cbd5e1;
          border-radius: 3px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #94a3b8;
        }
        
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slide-in {
          from { opacity: 0; transform: translateX(-20px); }
          to { opacity: 1; transform: translateX(0); }
        }
        
        @keyframes modal-in {
          from { opacity: 0; transform: scale(0.9) translateY(20px); }
          to { opacity: 1; transform: scale(1) translateY(0); }
        }
        
        .animate-fade-in {
          animation: fade-in 0.6s ease-out forwards;
        }
        
        .animate-slide-in {
          animation: slide-in 0.6s ease-out forwards;
        }
        
        .animate-modal-in {
          animation: modal-in 0.4s ease-out forwards;
        }
        
        .hover\\:scale-102:hover {
          transform: scale(1.02);
        }
        
        .hover\\:scale-105:hover {
          transform: scale(1.05);
        }
        
        .hover\\:shadow-3xl:hover {
          box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
        }
      `}</style>
    </div>
  );
};

export default ChatPage;