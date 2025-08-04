'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Send, Plus, Menu, X, MessageSquare, User, MoreVertical, FileText, File, Copy, Check, Bot, Upload, PaperclipIcon, LogOut } from 'lucide-react';

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
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Debug mode for development
  const DEBUG_STREAMING = process.env.NODE_ENV === 'development';

  // Get auth headers
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
  }, [messages, streamingMessage]);

  return (
    <div className="h-screen bg-white flex relative">
      {/* Mobile backdrop */}
      {(leftSidebarOpen || rightSidebarOpen) && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden"
          onClick={() => {
            setLeftSidebarOpen(false);
            setRightSidebarOpen(false);
          }}
        />
      )}
      
      {/* Left Sidebar - Chat History */}
      <div className={`${
        leftSidebarOpen ? 'w-64 md:w-64' : 'w-0'
      } transition-all duration-300 ease-in-out overflow-hidden bg-gray-900 flex flex-col ${
        leftSidebarOpen ? 'fixed md:relative z-40 md:z-auto h-full' : ''
      }`}>
        {/* Sidebar Header */}
        <div className="p-4 border-b border-gray-700">
          <button
            onClick={() => setShowNewSessionModal(true)}
            className="w-full flex items-center justify-center space-x-2 px-3 py-2 bg-white text-gray-900 rounded-lg hover:bg-gray-100 transition-colors font-medium"
          >
            <Plus className="w-4 h-4" />
            <span>New chat</span>
          </button>
        </div>

        {/* Chat Sessions */}
        <div className="flex-1 overflow-y-auto p-2">
          {sessions.map((session) => (
            <button
              key={session.id}
              onClick={() => switchSession(session)}
              className={`w-full text-left p-3 rounded-lg mb-1 transition-colors group relative ${
                currentSession?.id === session.id
                  ? 'bg-gray-800 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
            >
              <div className="flex items-center space-x-3">
                <MessageSquare className="w-4 h-4 flex-shrink-0" />
                <span className="truncate text-sm">{session.title}</span>
              </div>
            </button>
          ))}
        </div>

        {/* Sidebar Footer */}
        <div className="p-4 border-t border-gray-700">
          <div className="flex items-center space-x-3 text-gray-300">
            <User className="w-8 h-8 bg-gray-700 rounded-full p-2" />
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium truncate">User</div>
            </div>
            <button
              onClick={() => {
                localStorage.clear();
                window.location.href = '/login';
              }}
              className="p-1 hover:bg-gray-700 rounded"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            {!leftSidebarOpen && (
              <button
                onClick={() => setLeftSidebarOpen(true)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <Menu className="w-5 h-5" />
              </button>
            )}
            <h1 className="text-lg font-semibold text-gray-900">
              {currentSession?.title || 'ML Agent'}
            </h1>
            {activeFile && (
              <div className="flex items-center space-x-2 px-2 py-1 bg-green-100 text-green-800 rounded-md text-sm">
                <File className="w-3 h-3" />
                <span>{activeFile.file_name}</span>
              </div>
            )}
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setRightSidebarOpen(!rightSidebarOpen)}
              className="p-2 hover:bg-gray-100 rounded-lg"
            >
              <PaperclipIcon className="w-5 h-5" />
            </button>
            {leftSidebarOpen && (
              <button
                onClick={() => setLeftSidebarOpen(false)}
                className="p-2 hover:bg-gray-100 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto">
          {!currentSession ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <Bot className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h2 className="text-2xl font-semibold text-gray-700 mb-2">Welcome to ML Agent</h2>
                <p className="text-gray-500 mb-6">Your independent ML assistant for data analysis and insights</p>
                <button
                  onClick={() => setShowNewSessionModal(true)}
                  className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors"
                >
                  Start new conversation
                </button>
              </div>
            </div>
          ) : (
            <div className="max-w-3xl mx-auto px-4 py-6">
              {messages.map((message) => (
                <div key={message.id} className="mb-6">
                  <div className="flex items-start space-x-3">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      message.role === 'user' ? 'bg-gray-900' : 'bg-green-600'
                    }`}>
                      {message.role === 'user' ? (
                        <User className="w-4 h-4 text-white" />
                      ) : (
                        <Bot className="w-4 h-4 text-white" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-gray-900 mb-1">
                        {message.role === 'user' ? 'You' : 'ML Agent'}
                      </div>
                      <div className="text-gray-700">
                        {renderMessageContent(message.content, message.id)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              
              {/* Streaming message */}
              {isLoading && streamingMessage && (
                <div className="mb-6">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 rounded-full bg-green-600 flex items-center justify-center relative">
                      <Bot className="w-4 h-4 text-white" />
                      <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full animate-ping"></div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-1">
                        <div className="text-sm font-medium text-gray-900">ML Agent</div>
                        <div className="flex items-center space-x-1 text-xs text-green-600">
                          <div className="w-1 h-1 bg-green-500 rounded-full animate-pulse"></div>
                          <div className="w-1 h-1 bg-green-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                          <div className="w-1 h-1 bg-green-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                          <span>streaming</span>
                        </div>
                      </div>
                      <div className="text-gray-700">
                        {renderMessageContent(streamingMessage, 'streaming')}
                        <span className="inline-block w-2 h-5 bg-gray-400 animate-pulse ml-1">▋</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Loading indicator */}
              {isLoading && !streamingMessage && (
                <div className="mb-6">
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 rounded-full bg-green-600 flex items-center justify-center">
                      <Bot className="w-4 h-4 text-white animate-pulse" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-gray-900 mb-1">ML Agent</div>
                      <div className="flex items-center space-x-2 text-gray-500">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        <span>Analyzing your data...</span>
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
          <div className="border-t border-gray-200 p-4">
            <div className="max-w-3xl mx-auto">
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
                  placeholder={`Message ML Agent${activeFile ? ` about ${activeFile.file_name}` : ''}...`}
                  className="w-full p-3 pr-12 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent text-sm md:text-base"
                  rows={1}
                  style={{ minHeight: '44px', maxHeight: '200px' }}
                  onInput={(e) => {
                    const target = e.target as HTMLTextAreaElement;
                    target.style.height = 'auto';
                    target.style.height = Math.min(target.scrollHeight, 200) + 'px';
                  }}
                  disabled={isLoading}
                />
                <button
                  onClick={sendMessage}
                  disabled={!inputMessage.trim() || isLoading}
                  className="absolute right-2 bottom-2 p-2 bg-gray-900 text-white rounded-md hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Right Sidebar - Files */}
      <div className={`${
        rightSidebarOpen ? 'w-80 md:w-80' : 'w-0'
      } transition-all duration-300 ease-in-out overflow-hidden bg-gray-50 border-l border-gray-200 flex flex-col ${
        rightSidebarOpen ? 'fixed md:relative z-40 md:z-auto right-0 h-full' : ''
      }`}>
        {/* Files Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Dataset Files</h2>
            <button
              onClick={() => setRightSidebarOpen(false)}
              className="p-1 hover:bg-gray-200 rounded"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <button
            onClick={() => setShowUploadModal(true)}
            className="w-full flex items-center justify-center space-x-2 px-3 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors"
          >
            <Upload className="w-4 h-4" />
            <span>Upload dataset</span>
          </button>
        </div>

        {/* Files List */}
        <div className="flex-1 overflow-y-auto p-4">
          {loadingFiles ? (
            <div className="flex items-center justify-center py-8">
              <div className="w-6 h-6 border-2 border-gray-300 border-t-gray-900 rounded-full animate-spin"></div>
            </div>
          ) : files.length === 0 ? (
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">No datasets uploaded yet</p>
            </div>
          ) : (
            <div className="space-y-2">
              {files.map((file) => (
                <div
                  key={file.file_name}
                  onClick={() => currentSession && setActiveFileForSession(file.file_name || '')}
                  className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                    activeFile?.file_name === file.file_name
                      ? 'bg-green-50 border-green-200'
                      : 'bg-white border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <File className={`w-5 h-5 ${
                      activeFile?.file_name === file.file_name ? 'text-green-600' : 'text-gray-400'
                    }`} />
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-gray-900 truncate">
                        {file.file_name}
                      </div>
                      {file.description && (
                        <div className="text-sm text-gray-500 truncate">
                          {file.description}
                        </div>
                      )}
                      {file.size && (
                        <div className="text-xs text-gray-400">
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </div>
                      )}
                    </div>
                    {settingActiveFile === file.file_name && (
                      <div className="w-4 h-4 border-2 border-green-600 border-t-transparent rounded-full animate-spin"></div>
                    )}
                  </div>
                </div>
              ))}
            </div>
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
    </div>
  );
};

export default ChatPage;