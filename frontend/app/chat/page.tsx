'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Send, Plus, Menu, X, MessageSquare, User, MoreVertical, FileText, File, Copy, Check, Bot, Upload, PaperclipIcon, LogOut, Database, Zap, ArrowRight, Trash2 } from 'lucide-react';

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
  const router = useRouter();
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSession, setCurrentSession] = useState<Session | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [leftSidebarOpen, setLeftSidebarOpen] = useState(true);
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false);
  const [showNewSessionModal, setShowNewSessionModal] = useState(false);
  const [newSessionName, setNewSessionName] = useState('');
  const [newSessionError, setNewSessionError] = useState('');
  const [files, setFiles] = useState<FileItem[]>([]);
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
  const [copiedCode, setCopiedCode] = useState<string | null>(null);
  const [streamingMessage, setStreamingMessage] = useState('');
  const [showDeleteSessionModal, setShowDeleteSessionModal] = useState(false);
  const [sessionToDelete, setSessionToDelete] = useState<Session | null>(null);
  const [showDeleteFileModal, setShowDeleteFileModal] = useState(false);
  const [fileToDelete, setFileToDelete] = useState<FileItem | null>(null);
  const [deletingSession, setDeletingSession] = useState(false);
  const [deletingFile, setDeletingFile] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Debug mode for development
  const DEBUG_STREAMING = process.env.NODE_ENV === 'development';

  // Logout function
  const handleLogout = useCallback(() => {
    try {
      // Clear all localStorage data
      localStorage.removeItem('access_token');
      localStorage.removeItem('token_type');
      localStorage.removeItem('activeSessionId');
      localStorage.removeItem('activeSessionTitle');
      
      // Clear all state
      setSessions([]);
      setCurrentSession(null);
      setMessages([]);
      setFiles([]);
      setActiveFile(null);
      setInputMessage('');
      
      // Redirect to login page
      router.push('/login');
    } catch (error) {
      console.error('Error during logout:', error);
      // Fallback to window.location if router fails
      window.location.href = '/login';
    }
  }, [router]);

  // Get auth headers
  const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    const tokenType = localStorage.getItem('token_type') || 'Bearer';
    return {
      'Authorization': `${tokenType} ${token}`,
      'Content-Type': 'application/json',
    };
  };

  // Check if response indicates authentication failure
  const handleAuthError = useCallback((response: Response) => {
    if (response.status === 401 || response.status === 403) {
      console.log('Authentication failed, redirecting to login');
      handleLogout();
      return true;
    }
    return false;
  }, [handleLogout]);

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
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: content.slice(lastIndex, match.index)
        });
      }

      parts.push({
        type: 'code',
        language: match[1] || 'text',
        content: match[2].trim()
      });

      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < content.length) {
      parts.push({
        type: 'text',
        content: content.slice(lastIndex)
      });
    }

    return parts.length > 0 ? parts : [{ type: 'text', content }];
  };

  // Render message content with code highlighting
  const renderMessageContent = (content: string, messageId: string) => {
    const parts = parseMessageContent(content);
    
    return (
      <div className="prose max-w-none">
        {parts.map((part, index) => {
          if (part.type === 'code') {
            const codeId = `${messageId}-${index}`;
            return (
              <div key={index} className="my-4 first:mt-0 last:mb-0">
                <div className="bg-black rounded-t-lg px-4 py-2 flex items-center justify-between">
                  <span className="text-gray-400 text-sm font-mono">{part.language}</span>
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

      if (handleAuthError(response)) return;

      if (response.ok) {
        const data = await response.json();
        setSessions(data);
      } else {
        console.error('Failed to load sessions');
      }
    } catch (error) {
      console.error('Error loading sessions:', error);
    }
  }, [handleAuthError]);

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
      // Removed setLoadingActiveFile call
    }
  }, [currentSession]);

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
        await loadFiles();
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
        await loadFiles();
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

  // Create new session
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
        
        loadFiles();
        getActiveFile();
        
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

  // Switch session
  const switchSession = async (session: Session) => {
    if (currentSession?.id === session.id) return;

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
        loadFiles();
        getActiveFile();
        localStorage.setItem('activeSessionId', session.id);
        localStorage.setItem('activeSessionTitle', session.title);
      }
    } catch (error) {
      console.error('Error switching session:', error);
    }
  };

  // Delete session
  const deleteSession = async (session: Session) => {
    setSessionToDelete(session);
    setShowDeleteSessionModal(true);
  };

  const confirmDeleteSession = async () => {
    if (!sessionToDelete) return;

    setDeletingSession(true);
    try {
      // Based on UI requirements: DELETE to /api/v1/gateway/sessions/{title}
      const response = await fetch(`http://localhost:8003/api/v1/gateway/sessions/${sessionToDelete.title}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        // Remove session from list
        setSessions(prev => prev.filter(s => s.id !== sessionToDelete.id));
        
        // If this was the current session, switch to another or clear
        if (currentSession?.id === sessionToDelete.id) {
          const remainingSessions = sessions.filter(s => s.id !== sessionToDelete.id);
          if (remainingSessions.length > 0) {
            await switchSession(remainingSessions[0]);
          } else {
            setCurrentSession(null);
            setMessages([]);
            setActiveFile(null);
          }
        }
      } else {
        console.error('Failed to delete session');
      }
    } catch (error) {
      console.error('Error deleting session:', error);
    } finally {
      setDeletingSession(false);
      setShowDeleteSessionModal(false);
      setSessionToDelete(null);
    }
  };

  // Delete file
  const deleteFile = async (file: FileItem) => {
    setFileToDelete(file);
    setShowDeleteFileModal(true);
  };

  const confirmDeleteFile = async () => {
    if (!fileToDelete) return;

    setDeletingFile(true);
    try {
      // Based on UI requirements: DELETE to /api/v1/gateway/files/{file_name}
      const response = await fetch(`http://localhost:8003/api/v1/gateway/files/${fileToDelete.file_name}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      if (response.ok) {
        // Remove file from list
        setFiles(prev => prev.filter(f => f.file_name !== fileToDelete.file_name));
        
        // If this was the active file, clear it
        if (activeFile?.file_name === fileToDelete.file_name) {
          setActiveFile(null);
        }
      } else {
        console.error('Failed to delete file');
      }
    } catch (error) {
      console.error('Error deleting file:', error);
    } finally {
      setDeletingFile(false);
      setShowDeleteFileModal(false);
      setFileToDelete(null);
    }
  };

  // Send message with streaming
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
    setStreamingMessage('');

    try {
      if (DEBUG_STREAMING) {
        console.log('Starting streaming request to:', `http://localhost:8003/api/v1/gateway/chat/stream?question=${encodeURIComponent(currentQuestion)}`);
      }
      
      const response = await fetch(`http://localhost:8003/api/v1/gateway/chat/stream?question=${encodeURIComponent(currentQuestion)}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (DEBUG_STREAMING) {
        console.log('Stream response status:', response.status, 'OK:', response.ok);
        console.log('Stream response headers:', Object.fromEntries(response.headers.entries()));
      }

      if (handleAuthError(response)) {
        setIsLoading(false);
        return;
      }

      if (response.ok && response.body) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullContent = '';

        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            // Decode the chunk - this is plain text from the ML agent
            const chunk = decoder.decode(value, { stream: true });
            if (DEBUG_STREAMING) {
              console.log('Received chunk:', JSON.stringify(chunk));
            }
            
            // Simply append the chunk to the full content
            fullContent += chunk;
            setStreamingMessage(fullContent);
          }
        } catch (readError) {
          console.error('Error reading stream:', readError);
          // If streaming fails, fall back to regular chat
          throw readError;
        }

        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: fullContent || 'No response received',
          role: 'assistant',
          timestamp: new Date().toISOString(),
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        // Fallback to regular chat endpoint
        const fallbackResponse = await fetch(`http://localhost:8003/api/v1/gateway/chat/?question=${encodeURIComponent(currentQuestion)}`, {
          method: 'GET',
          headers: getAuthHeaders(),
        });

        if (fallbackResponse.ok) {
          const contentType = fallbackResponse.headers.get('content-type');
          let content;
          
          if (contentType && contentType.includes('application/json')) {
            const data = await fallbackResponse.json();
            content = data.response || data.message || data.answer || JSON.stringify(data);
          } else {
            content = await fallbackResponse.text();
          }
          
          const assistantMessage: Message = {
            id: (Date.now() + 1).toString(),
            content: content || 'No response received',
            role: 'assistant',
            timestamp: new Date().toISOString(),
          };
          setMessages(prev => [...prev, assistantMessage]);
        } else {
          throw new Error('Failed to get response');
        }
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
      setStreamingMessage('');
    }
  };

  // Initialize sessions
  const initializeSessions = useCallback(async () => {
    await loadSessions();
    // Load files initially
    await loadFiles();
  }, [loadSessions, loadFiles]);

  // Restore active session after sessions are loaded
  const restoreActiveSession = useCallback(async () => {
    const savedSessionId = localStorage.getItem('activeSessionId');
    const savedSessionTitle = localStorage.getItem('activeSessionTitle');
    
    if (savedSessionId && savedSessionTitle && sessions.length > 0) {
      const savedSession = sessions.find(s => s.id === savedSessionId && s.title === savedSessionTitle);
      if (savedSession) {
        setCurrentSession(savedSession);
        loadMessages(savedSession.id);
        getActiveFile();
      } else {
        localStorage.removeItem('activeSessionId');
        localStorage.removeItem('activeSessionTitle');
      }
    }
  }, [sessions, loadMessages, getActiveFile]);

  // Check if user is authenticated and initialize
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      return;
    }
    
    initializeSessions();
  }, [initializeSessions, router]);

  // Restore active session after sessions are loaded
  useEffect(() => {
    if (sessions.length > 0) {
      restoreActiveSession();
    }
  }, [sessions, restoreActiveSession]);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingMessage]);

  return (
    <div className="h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex relative">
      {/* Mobile backdrop */}
      {(leftSidebarOpen || rightSidebarOpen) && (
        <div 
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 md:hidden transition-all duration-300"
          onClick={() => {
            setLeftSidebarOpen(false);
            setRightSidebarOpen(false);
          }}
        />
      )}
      
      {/* Left Sidebar - Chat History */}
      <div className={`${
        leftSidebarOpen ? 'w-72 md:w-72' : 'w-0'
      } transition-all duration-500 ease-in-out overflow-hidden bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 flex flex-col ${
        leftSidebarOpen ? 'fixed md:relative z-40 md:z-auto h-full shadow-2xl' : ''
      } border-r border-slate-700/50`}>
        {/* Sidebar Header */}
        <div className="p-6 border-b border-slate-700/50 bg-slate-800/50">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-white font-bold text-lg">ML Agent</h1>
                <p className="text-slate-400 text-xs">Intelligent Data Assistant</p>
              </div>
            </div>
            <button
              onClick={() => setLeftSidebarOpen(false)}
              className="p-1.5 hover:bg-slate-700/50 rounded-lg transition-all duration-200 group"
              title="Close sidebar"
            >
              <X className="w-4 h-4 text-slate-400 group-hover:text-white" />
            </button>
          </div>
          <button
            onClick={() => setShowNewSessionModal(true)}
            className="w-full flex items-center justify-center space-x-3 px-4 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-2xl transition-all duration-300 font-medium shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98]"
          >
            <Plus className="w-4 h-4" />
            <span>New Chat</span>
            <div className="w-1 h-1 bg-white/30 rounded-full"></div>
          </button>
        </div>

        {/* Chat Sessions */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          <div className="text-slate-400 text-xs font-medium uppercase tracking-wider mb-4 px-2">
            Recent Conversations
          </div>
          {sessions.map((session, index) => (
            <div
              key={session.id}
              className="opacity-0 animate-fade-in"
              style={{ animationDelay: `${index * 0.05}s`, animationFillMode: 'forwards' }}
            >
              <div className={`w-full text-left p-4 rounded-2xl transition-all duration-300 group relative overflow-hidden ${
                currentSession?.id === session.id
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg transform scale-[1.02]'
                  : 'text-slate-300 hover:bg-slate-800/70 hover:text-white hover:shadow-lg hover:transform hover:scale-[1.01]'
              } backdrop-blur-sm border border-slate-700/30 hover:border-slate-600/50`}>
                <div className="flex items-center space-x-3">
                  <div className={`w-2 h-2 rounded-full transition-all duration-300 ${
                    currentSession?.id === session.id 
                      ? 'bg-white shadow-lg' 
                      : 'bg-slate-500 group-hover:bg-blue-400'
                  }`} />
                  <div 
                    className="min-w-0 flex-1 cursor-pointer"
                    onClick={() => switchSession(session)}
                  >
                    <span className="text-sm font-medium truncate block leading-5">
                      {session.title}
                    </span>
                    <span className="text-xs opacity-70 truncate block">
                      {new Date(session.created_at).toLocaleDateString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <MessageSquare className="w-4 h-4 opacity-60 group-hover:opacity-100 transition-opacity" />
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteSession(session);
                      }}
                      className="p-1 rounded-lg opacity-0 group-hover:opacity-100 hover:bg-red-500/20 hover:text-red-400 transition-all duration-200"
                      title="Delete session"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                {/* Active session indicator */}
                {currentSession?.id === session.id && (
                  <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-1 h-8 bg-white rounded-r-full shadow-lg" />
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Sidebar Footer */}
        <div className="p-6 border-t border-slate-700/50 bg-slate-800/30">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-slate-600 to-slate-700 rounded-2xl flex items-center justify-center shadow-lg">
              <User className="w-5 h-5 text-slate-300" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-white font-medium text-sm">User</div>
              <div className="text-slate-400 text-xs">Free Plan</div>
            </div>
            <button
              onClick={handleLogout}
              className="p-2 hover:bg-slate-700 rounded-xl transition-all duration-200 text-slate-400 hover:text-white group"
              title="Sign out"
            >
              <LogOut className="w-4 h-4 group-hover:scale-110 transition-transform" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col bg-white/70 backdrop-blur-sm">
        {/* Header */}
        <div className="bg-white/80 backdrop-blur-md border-b border-slate-200/60 px-6 py-4 flex items-center justify-between shadow-sm">
          <div className="flex items-center space-x-4">
            {!leftSidebarOpen && (
              <button
                onClick={() => setLeftSidebarOpen(true)}
                className="p-2.5 hover:bg-slate-100 rounded-2xl transition-all duration-200 group"
              >
                <Menu className="w-5 h-5 text-slate-600 group-hover:text-slate-800" />
              </button>
            )}
            <div className="flex items-center space-x-3">
              <h1 className="text-xl font-bold text-slate-800">
                {currentSession?.title || 'ML Agent'}
              </h1>
              {activeFile && (
                <div className="flex items-center space-x-2 px-3 py-1.5 bg-gradient-to-r from-emerald-100 to-green-100 text-emerald-700 rounded-2xl text-sm font-medium shadow-sm border border-emerald-200/50">
                  <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                  <File className="w-3.5 h-3.5" />
                  <span className="font-semibold">{activeFile.file_name}</span>
                </div>
              )}
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setRightSidebarOpen(!rightSidebarOpen)}
              className={`p-2.5 rounded-2xl transition-all duration-200 group ${
                rightSidebarOpen 
                  ? 'bg-blue-100 text-blue-600' 
                  : 'hover:bg-slate-100 text-slate-600 hover:text-slate-800'
              }`}
              title="Dataset Files"
            >
              <PaperclipIcon className="w-5 h-5" />
            </button>
            {leftSidebarOpen && (
              <button
                onClick={() => setLeftSidebarOpen(false)}
                className="p-2.5 hover:bg-slate-100 rounded-2xl transition-all duration-200 group"
                title="Close sidebar"
              >
                <X className="w-5 h-5 text-slate-600 group-hover:text-slate-800" />
              </button>
            )}
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto bg-gradient-to-b from-slate-50/50 to-white/80">
          {!currentSession ? (
            <div className="h-full flex items-center justify-center p-8">
              <div className="text-center max-w-2xl">
                <div className="mb-8">
                  <div className="w-20 h-20 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-2xl animate-pulse">
                    <Bot className="w-10 h-10 text-white" />
                  </div>
                  <h2 className="text-4xl font-bold text-slate-800 mb-4">
                    Welcome to <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">ML Agent</span>
                  </h2>
                  <p className="text-xl text-slate-600 mb-8 leading-relaxed">
                    Your independent AI assistant for advanced data analysis, insights, and machine learning solutions
                  </p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                  <div className="bg-white/80 backdrop-blur-sm rounded-3xl p-6 shadow-lg border border-slate-200/50 hover:shadow-xl transition-all duration-300 hover:scale-105">
                    <div className="w-12 h-12 bg-gradient-to-r from-amber-400 to-orange-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg">
                      <Database className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-800 mb-2">Data Analysis</h3>
                    <p className="text-slate-600 text-sm">Upload your datasets and get instant insights, visualizations, and statistical analysis</p>
                  </div>
                  
                  <div className="bg-white/80 backdrop-blur-sm rounded-3xl p-6 shadow-lg border border-slate-200/50 hover:shadow-xl transition-all duration-300 hover:scale-105">
                    <div className="w-12 h-12 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-2xl flex items-center justify-center mb-4 shadow-lg">
                      <Zap className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-800 mb-2">Smart Insights</h3>
                    <p className="text-slate-600 text-sm">AI-powered recommendations and predictive analytics for your business decisions</p>
                  </div>
                </div>
                
                <button
                  onClick={() => setShowNewSessionModal(true)}
                  className="inline-flex items-center space-x-3 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold rounded-2xl transition-all duration-300 shadow-xl hover:shadow-2xl transform hover:scale-105 active:scale-95"
                >
                  <Plus className="w-5 h-5" />
                  <span>Start New Conversation</span>
                  <ArrowRight className="w-5 h-5" />
                </button>
              </div>
            </div>
          ) : (
            <div className="max-w-4xl mx-auto px-6 py-8 space-y-8">
              {messages.map((message, index) => (
                <div 
                  key={message.id} 
                  className="opacity-0 animate-fade-in"
                  style={{ animationDelay: `${index * 0.1}s`, animationFillMode: 'forwards' }}
                >
                  <div className={`flex items-start space-x-4 ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    <div className={`w-10 h-10 rounded-2xl flex items-center justify-center shadow-lg ${
                      message.role === 'user' 
                        ? 'bg-gradient-to-r from-blue-600 to-indigo-600' 
                        : 'bg-gradient-to-r from-emerald-500 to-teal-600'
                    }`}>
                      {message.role === 'user' ? (
                        <User className="w-5 h-5 text-white" />
                      ) : (
                        <Bot className="w-5 h-5 text-white" />
                      )}
                    </div>
                    <div className={`flex-1 min-w-0 ${message.role === 'user' ? 'text-right' : ''}`}>
                      <div className="flex items-center space-x-2 mb-3">
                        <span className="text-sm font-bold text-slate-700">
                          {message.role === 'user' ? 'You' : 'ML Agent'}
                        </span>
                        <span className="text-xs text-slate-400">
                          {new Date(message.timestamp).toLocaleTimeString('en-US', {
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </span>
                      </div>
                      <div className={`${
                        message.role === 'user'
                          ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-3xl rounded-br-lg shadow-lg px-6 py-4'
                          : 'bg-white/80 backdrop-blur-sm border border-slate-200/60 rounded-3xl rounded-bl-lg shadow-lg overflow-hidden'
                      }`}>
                        <div className={`${message.role === 'user' ? 'text-white' : 'text-slate-800'}`}>
                          {renderMessageContent(message.content, message.id)}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              
              {/* Streaming message */}
              {isLoading && streamingMessage && (
                <div className="animate-fade-in">
                  <div className="flex items-start space-x-4">
                    <div className="w-10 h-10 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg relative">
                      <Bot className="w-5 h-5 text-white" />
                      <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full animate-ping"></div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-3 mb-3">
                        <span className="text-sm font-bold text-slate-700">ML Agent</span>
                        <div className="flex items-center space-x-2 px-2 py-1 bg-emerald-100 text-emerald-700 rounded-full text-xs font-medium">
                          <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></div>
                          <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                          <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                          <span>Streaming</span>
                        </div>
                      </div>
                      <div className="bg-white/80 backdrop-blur-sm border border-slate-200/60 rounded-3xl rounded-bl-lg shadow-lg overflow-hidden">
                        <div className="text-slate-800 p-6">
                          {renderMessageContent(streamingMessage, 'streaming')}
                          <span className="inline-block w-2 h-5 bg-emerald-500 animate-pulse ml-1 rounded-sm">▋</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Loading indicator */}
              {isLoading && !streamingMessage && (
                <div className="animate-fade-in">
                  <div className="flex items-start space-x-4">
                    <div className="w-10 h-10 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 flex items-center justify-center shadow-lg">
                      <Bot className="w-5 h-5 text-white animate-pulse" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-3">
                        <span className="text-sm font-bold text-slate-700">ML Agent</span>
                      </div>
                      <div className="bg-white/80 backdrop-blur-sm border border-slate-200/60 rounded-3xl rounded-bl-lg shadow-lg p-6">
                        <div className="flex items-center space-x-3 text-slate-600">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          </div>
                          <span className="font-medium">Analyzing your data and preparing insights...</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        {currentSession && (
          <div className="border-t border-slate-200/60 bg-white/80 backdrop-blur-md p-6">
            <div className="max-w-4xl mx-auto">
              <div className="relative">
                <div className="flex items-end space-x-4 bg-white/90 backdrop-blur-sm rounded-3xl border border-slate-200/60 shadow-lg p-2 focus-within:ring-2 focus-within:ring-blue-500/20 focus-within:border-blue-500/50 transition-all duration-200">
                  <div className="flex-1">
                    <textarea
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                          e.preventDefault();
                          sendMessage();
                        }
                      }}
                      placeholder={`Ask ML Agent${activeFile ? ` about ${activeFile.file_name}` : ' anything about your data'}...`}
                      className="w-full p-4 bg-transparent border-none resize-none focus:outline-none text-slate-800 placeholder-slate-500 text-base leading-6"
                      rows={1}
                      style={{ minHeight: '24px', maxHeight: '160px' }}
                      onInput={(e) => {
                        const target = e.target as HTMLTextAreaElement;
                        target.style.height = 'auto';
                        target.style.height = Math.min(target.scrollHeight, 160) + 'px';
                      }}
                      disabled={isLoading}
                    />
                  </div>
                  <button
                    onClick={sendMessage}
                    disabled={!inputMessage.trim() || isLoading}
                    className={`p-3 rounded-2xl transition-all duration-200 shadow-lg ${
                      inputMessage.trim() && !isLoading
                        ? 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-blue-500/25 hover:shadow-blue-500/40 transform hover:scale-105 active:scale-95'
                        : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                    }`}
                  >
                    {isLoading ? (
                      <div className="w-5 h-5 border-2 border-slate-400 border-t-transparent rounded-full animate-spin" />
                    ) : (
                      <Send className="w-5 h-5" />
                    )}
                  </button>
                </div>
                
                {/* Helper text */}
                <div className="flex items-center justify-center space-x-4 mt-3 text-xs text-slate-500">
                  <div className="flex items-center space-x-1">
                    <Bot className="w-3 h-3" />
                    <span>AI-powered data analysis</span>
                  </div>
                  {activeFile?.file_name && (
                    <>
                      <span>•</span>
                      <div className="flex items-center space-x-1">
                        <File className="w-3 h-3 text-emerald-600" />
                        <span className="text-emerald-600 font-medium">{activeFile.file_name}</span>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Right Sidebar - Files */}
      <div className={`${
        rightSidebarOpen ? 'w-96 md:w-96' : 'w-0'
      } transition-all duration-500 ease-in-out overflow-hidden bg-gradient-to-b from-slate-50 to-white border-l border-slate-200/60 flex flex-col ${
        rightSidebarOpen ? 'fixed md:relative z-40 md:z-auto right-0 h-full shadow-2xl' : ''
      }`}>
        {/* Files Header */}
        <div className="p-6 border-b border-slate-200/60 bg-white/80 backdrop-blur-sm">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg">
                <Database className="w-5 h-5 text-white" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-slate-800">Dataset Files</h2>
                <p className="text-xs text-slate-500">
                  {files.length} file{files.length !== 1 ? 's' : ''} available
                </p>
              </div>
            </div>
            <button
              onClick={() => setRightSidebarOpen(false)}
              className="p-2 hover:bg-slate-100 rounded-2xl transition-all duration-200 group"
            >
              <X className="w-5 h-5 text-slate-600 group-hover:text-slate-800" />
            </button>
          </div>
          <button
            onClick={() => setShowUploadModal(true)}
            className="w-full flex items-center justify-center space-x-3 px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white rounded-2xl transition-all duration-300 font-medium shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98]"
          >
            <Upload className="w-4 h-4" />
            <span>Upload Dataset</span>
            <div className="w-1 h-1 bg-white/30 rounded-full"></div>
          </button>
        </div>

        {/* Files List */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {loadingFiles ? (
            <div className="flex items-center justify-center py-12">
              <div className="flex flex-col items-center space-y-4">
                <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-slate-600 font-medium">Loading datasets...</p>
              </div>
            </div>
          ) : files.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-slate-100 rounded-3xl flex items-center justify-center mx-auto mb-6">
                <FileText className="w-8 h-8 text-slate-400" />
              </div>
              <h3 className="text-lg font-semibold text-slate-700 mb-2">No datasets yet</h3>
              <p className="text-slate-500 text-sm leading-relaxed">
                Upload your first dataset to start analyzing data with ML Agent
              </p>
            </div>
          ) : (
            <>
              <div className="text-slate-400 text-xs font-medium uppercase tracking-wider mb-4 px-2">
                Available Datasets
              </div>
              <div className="space-y-3">
                {files.map((file, index) => (
                  <div
                    key={file.file_name}
                    className="opacity-0 animate-fade-in"
                    style={{ animationDelay: `${index * 0.05}s`, animationFillMode: 'forwards' }}
                  >
                    <div className={`group relative p-4 rounded-2xl border transition-all duration-300 overflow-hidden ${
                        activeFile?.file_name === file.file_name
                          ? 'bg-gradient-to-r from-emerald-50 to-green-50 border-emerald-200 shadow-lg transform scale-[1.02]'
                          : 'bg-white/80 backdrop-blur-sm border-slate-200/60 hover:border-slate-300 hover:shadow-lg hover:bg-white hover:transform hover:scale-[1.01]'
                      }`}
                    >
                      <div className="flex items-start space-x-4">
                        <div className={`w-12 h-12 rounded-2xl flex items-center justify-center shadow-md transition-all duration-300 ${
                          activeFile?.file_name === file.file_name 
                            ? 'bg-gradient-to-r from-emerald-500 to-green-600 text-white' 
                            : 'bg-slate-100 text-slate-600 group-hover:bg-slate-200'
                        }`}>
                          <File className="w-6 h-6" />
                        </div>
                        <div 
                          className="flex-1 min-w-0 cursor-pointer"
                          onClick={() => currentSession && setActiveFileForSession(file.file_name || '')}
                        >
                          <div className="flex items-center space-x-2 mb-1">
                            <span className="font-bold text-slate-800 truncate">
                              {file.file_name}
                            </span>
                            {activeFile?.file_name === file.file_name && (
                              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
                            )}
                          </div>
                          {file.description && (
                            <p className="text-sm text-slate-600 truncate mb-2 leading-5">
                              {file.description}
                            </p>
                          )}
                          <div className="flex items-center space-x-3 text-xs">
                            {file.size && (
                              <span className="text-slate-500 font-medium">
                                {(file.size / 1024 / 1024).toFixed(1)} MB
                              </span>
                            )}
                            {file.upload_time && (
                              <span className="text-slate-400">
                                {new Date(file.upload_time).toLocaleDateString('en-US', {
                                  month: 'short',
                                  day: 'numeric'
                                })}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          {settingActiveFile === file.file_name && (
                            <div className="w-5 h-5 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
                          )}
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              deleteFile(file);
                            }}
                            className="p-2 rounded-lg opacity-0 group-hover:opacity-100 hover:bg-red-500/20 hover:text-red-500 transition-all duration-200"
                            title="Delete file"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                      
                      {/* Active indicator */}
                      {activeFile?.file_name === file.file_name && (
                        <div className="absolute left-0 top-1/2 transform -translate-y-1/2 w-1 h-12 bg-emerald-500 rounded-r-full shadow-lg"></div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>

      {/* New Session Modal */}
      {showNewSessionModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">New Chat</h2>
            <input
              type="text"
              value={newSessionName}
              onChange={(e) => {
                setNewSessionName(e.target.value);
                if (newSessionError) setNewSessionError('');
              }}
              placeholder="Enter chat name..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent mb-4"
              autoFocus
            />
            {newSessionError && (
              <p className="text-red-600 text-sm mb-4">{newSessionError}</p>
            )}
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setShowNewSessionModal(false);
                  setNewSessionName('');
                  setNewSessionError('');
                }}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => createNewSession(newSessionName)}
                disabled={!newSessionName.trim()}
                className="flex-1 px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Upload File Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Upload Dataset</h2>
            
            <div className="space-y-4">
              {!selectedFile ? (
                <div 
                  onClick={() => fileInputRef.current?.click()}
                  className="w-full p-8 border-2 border-dashed border-gray-300 rounded-lg text-center cursor-pointer hover:border-gray-400 transition-colors"
                >
                  <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-gray-600">Click to select a file</p>
                  <p className="text-sm text-gray-500 mt-1">CSV, JSON, TXT, etc.</p>
                </div>
              ) : (
                <div className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center space-x-3">
                    <File className="w-5 h-5 text-gray-600" />
                    <div>
                      <div className="font-medium text-gray-900">{selectedFile.name}</div>
                      <div className="text-sm text-gray-500">
                        {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                      </div>
                    </div>
                  </div>
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

              <input
                type="text"
                value={fileName}
                onChange={(e) => setFileName(e.target.value)}
                placeholder="Dataset name..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
              />

              <textarea
                value={fileDescription}
                onChange={(e) => setFileDescription(e.target.value)}
                placeholder="Description (optional)..."
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent resize-none"
                rows={3}
              />

              {uploadingFile && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Uploading...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-gray-900 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                </div>
              )}

              {uploadError && (
                <p className="text-red-600 text-sm">{uploadError}</p>
              )}
            </div>

            <div className="flex space-x-3 mt-6">
              <button
                onClick={() => {
                  setShowUploadModal(false);
                  setSelectedFile(null);
                  setFileName('');
                  setFileDescription('');
                  setUploadError('');
                }}
                disabled={uploadingFile}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={uploadFile}
                disabled={!selectedFile || !fileName.trim() || uploadingFile}
                className="flex-1 px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {uploadingFile ? 'Uploading...' : 'Upload'}
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Delete Session Confirmation Modal */}
      {showDeleteSessionModal && sessionToDelete && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4 animate-modal-in">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Delete Session</h2>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete the session <strong>&ldquo;{sessionToDelete.title}&rdquo;</strong>? 
              This action cannot be undone and all messages in this session will be permanently lost.
            </p>
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setShowDeleteSessionModal(false);
                  setSessionToDelete(null);
                }}
                disabled={deletingSession}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDeleteSession}
                disabled={deletingSession}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-red-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {deletingSession ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Deleting...
                  </>
                ) : (
                  'Delete Session'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Delete File Confirmation Modal */}
      {showDeleteFileModal && fileToDelete && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4 animate-modal-in">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Delete File</h2>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete the file <strong>&ldquo;{fileToDelete.file_name}&rdquo;</strong>? 
              This action cannot be undone and the file will be permanently removed from your account.
            </p>
            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setShowDeleteFileModal(false);
                  setFileToDelete(null);
                }}
                disabled={deletingFile}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDeleteFile}
                disabled={deletingFile}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-red-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {deletingFile ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Deleting...
                  </>
                ) : (
                  'Delete File'
                )}
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Enhanced CSS Animations */}
      <style jsx>{`
        @keyframes fade-in {
          from { 
            opacity: 0; 
            transform: translateY(10px); 
          }
          to { 
            opacity: 1; 
            transform: translateY(0); 
          }
        }
        
        @keyframes slide-in {
          from { 
            opacity: 0; 
            transform: translateX(-10px); 
          }
          to { 
            opacity: 1; 
            transform: translateX(0); 
          }
        }
        
        @keyframes modal-in {
          from { 
            opacity: 0; 
            transform: scale(0.95) translateY(10px); 
          }
          to { 
            opacity: 1; 
            transform: scale(1) translateY(0); 
          }
        }
        
        .animate-fade-in {
          animation: fade-in 0.6s ease-out forwards;
        }
        
        .animate-slide-in {
          animation: slide-in 0.5s ease-out forwards;
        }
        
        .animate-modal-in {
          animation: modal-in 0.3s ease-out forwards;
        }
        
        /* Custom scrollbar */
        .overflow-y-auto::-webkit-scrollbar {
          width: 6px;
        }
        
        .overflow-y-auto::-webkit-scrollbar-track {
          background: transparent;
        }
        
        .overflow-y-auto::-webkit-scrollbar-thumb {
          background: rgba(148, 163, 184, 0.4);
          border-radius: 3px;
        }
        
        .overflow-y-auto::-webkit-scrollbar-thumb:hover {
          background: rgba(148, 163, 184, 0.6);
        }
        
        /* Backdrop blur for better glass effect */
        .backdrop-blur-sm {
          backdrop-filter: blur(8px);
        }
        
        .backdrop-blur-md {
          backdrop-filter: blur(12px);
        }
        
        .backdrop-blur-xl {
          backdrop-filter: blur(20px);
        }
      `}</style>
    </div>
  );
};

export default ChatPage;